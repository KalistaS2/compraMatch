import json
import os
import random
import time
from dotenv import load_dotenv
from openai import OpenAI
from google import genai
from google.genai import types

# Carrega variáveis do .env
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env'))

# ── Carrega itens diretamente (evita import circular com construcao/similaridadeBase) ──

def carregar_itens_complexos():
    """Carrega itens do arquivo itens_complexos.json"""
    complexos_path = os.path.join(os.path.dirname(__file__), '../json/itens_complexos.json')
    try:
        with open(complexos_path, 'r', encoding='utf-8') as f:
            dados = json.load(f)
        return dados.get('itens', [])
    except FileNotFoundError:
        print(f"Erro: Arquivo {complexos_path} não encontrado")
        return []
    except json.JSONDecodeError:
        print("Erro: Arquivo JSON inválido")
        return []

# Caminhos de saída
OUTPUT_GPT = os.path.join(os.path.dirname(__file__), '../json/array_similaridade_gpt_llm.json')
OUTPUT_GEMINI = os.path.join(os.path.dirname(__file__), '../json/array_similaridade_gemini_llm.json')

PROMPT_TEMPLATE = (
    "Você é um especialista em análise de itens de licitação pública.\n\n"
    "Seu trabalho é comparar um item específico com TODOS os itens de uma lista e determinar similaridade.\n\n"
    "ITEM A ANALISAR:\n"
    "{item_analisar}\n\n"
    "LISTA DE ITENS PARA COMPARAÇÃO (JSON):\n"
    "{lista_itens_json}\n\n"
    "INSTRUÇÃO:\n"
    "Analise o 'ITEM A ANALISAR' e compare-o com CADA UM dos itens na lista acima.\n"
    "Retorne SOMENTE os itens que são SIMILARES ao item analisado (similar=1).\n"
    "NÃO inclua itens que NÃO são similares.\n\n"
    "Retorne APENAS um array JSON (sem formatação markdown) neste exato formato:\n"
    "[\n"
    "  {{\"nome_item\": \"<nome do item similar>\", \"similar\": 1}},\n"
    "  {{\"nome_item\": \"<nome do item similar>\", \"similar\": 1}},\n"
    "  ...\n"
    "]\n\n"
    "Se NENHUM item for similar, retorne uma lista vazia: []\n\n"
    "IMPORTANTE: Retorne apenas o JSON, sem nenhum texto adicional."
)

SAMPLE_SIZE = 335
MAX_RETRIES = 3
SEED = 42
CHUNK_SIZE = 500  # Itens por requisição (evita truncamento de resposta)


def _selecionar_itens(itens, seed=SEED, n=SAMPLE_SIZE):
    """Seleciona aleatoriamente `n` itens da lista."""
    random.seed(seed)
    indices = random.sample(range(len(itens)), min(n, len(itens)))
    return indices


def _chunkar_itens(itens, chunk_size=CHUNK_SIZE):
    """Divide a lista de itens em chunks de tamanho chunk_size."""
    for i in range(0, len(itens), chunk_size):
        yield itens[i:i + chunk_size]


def _parse_resposta(resposta_texto):
    """Extrai array de similaridades do JSON retornado pela LLM."""
    try:
        resposta_texto = resposta_texto.strip()
        # Remove markdown code blocks se existir
        if resposta_texto.startswith("```"):
            resposta_texto = resposta_texto.split("```")[1]
            if resposta_texto.startswith("json"):
                resposta_texto = resposta_texto[4:]
            resposta_texto = resposta_texto.strip()
        
        resultado = json.loads(resposta_texto)
        
        # Valida se é uma lista
        if isinstance(resultado, list):
            return resultado
        else:
            print(f"ERRO: Resposta não é uma lista. Tipo: {type(resultado)}")
            return []
    except json.JSONDecodeError as e:
        print(f"ERRO ao fazer parse do JSON: {e}")
        print(f"Texto recebido: {resposta_texto[:200]}...")
        return []
    except Exception as e:
        print(f"ERRO inesperado ao fazer parse: {e}")
        return []


def _salvar_progresso(resultado, output_path):
    """Salva o resultado parcial em disco."""
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(resultado, f, ensure_ascii=False, indent=2)


# ────────────────────────────── GPT ──────────────────────────────

def similaridade_gpt(api_key=None, model="gpt-4o-mini"):
    """
    Seleciona 335 itens aleatórios de itens_complexos.json e compara cada um
    com TODOS os outros itens usando a API do GPT, dividindo em chunks para
    evitar truncamento de resposta.
    Salva o resultado em json/array_similaridade_gpt_llm.json.
    
    Retorna apenas itens similares (similar=1) para cada item analisado.
    """
    print("="*60)
    print("[GPT] Iniciando função similaridade_gpt")
    print(f"[GPT] Modelo: {model}")
    print(f"[GPT] Modo: chunks de {CHUNK_SIZE} itens por requisição (retorna só similares)")
    print("="*60)

    if api_key is None:
        api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("API key do OpenAI não fornecida. Defina OPENAI_API_KEY ou passe como parâmetro.")
    print("[GPT] API key configurada com sucesso")

    print("[GPT] Inicializando cliente OpenAI...")
    client = OpenAI(api_key=api_key)
    print("[GPT] Cliente OpenAI inicializado")

    print("[GPT] Carregando itens complexos do JSON...")
    itens = carregar_itens_complexos()

    if not itens:
        print("[GPT] ERRO: Nenhum item encontrado. Abortando.")
        return []
    print(f"[GPT] Itens carregados com sucesso: {len(itens)} itens")

    # Divide itens em chunks
    chunks = list(_chunkar_itens(itens, CHUNK_SIZE))
    total_chunks = len(chunks)
    print(f"[GPT] Itens divididos em {total_chunks} chunks de até {CHUNK_SIZE} itens")

    print(f"[GPT] Selecionando {SAMPLE_SIZE} itens aleatórios (seed={SEED})...")
    indices_selecionados = _selecionar_itens(itens)
    total_itens = len(itens)
    total_selecionados = len(indices_selecionados)
    total_requisicoes = total_selecionados * total_chunks
    print(f"[GPT] Total de itens no dataset: {total_itens}")
    print(f"[GPT] Total de itens selecionados: {total_selecionados}")
    print(f"[GPT] Total de REQUISIÇÕES a fazer: {total_requisicoes} ({total_selecionados} itens × {total_chunks} chunks)")
    print(f"[GPT] Índices selecionados (primeiros 10): {indices_selecionados[:10]}...")
    print(f"[GPT] Arquivo de saída: {OUTPUT_GPT}")
    print("-"*60)

    resultado_itens = []
    tempo_inicio_total = time.time()
    requisicoes_realizadas = 0
    erros_total = 0

    for pos, i in enumerate(indices_selecionados):
        item_analisar = itens[i]
        nome_item = item_analisar.get("nome_item", "")
        classe_item = item_analisar.get("classe_item", "")
        tempo_inicio_item = time.time()
        
        print(f"\n[GPT] ── Item {pos + 1}/{total_selecionados} (índice {i}) ──")
        print(f"[GPT]   Nome: {nome_item}")
        print(f"[GPT]   Classe: {classe_item}")

        similaridades_totais = []

        for chunk_idx, chunk in enumerate(chunks):
            chunk_json = json.dumps(chunk, ensure_ascii=False, indent=2)
            print(f"[GPT]   Chunk {chunk_idx + 1}/{total_chunks} ({len(chunk)} itens, {len(chunk_json)} chars)... ", end="", flush=True)

            prompt = PROMPT_TEMPLATE.format(
                item_analisar=json.dumps(item_analisar, ensure_ascii=False),
                lista_itens_json=chunk_json
            )

            resposta = None
            for tentativa in range(MAX_RETRIES):
                try:
                    if tentativa > 0:
                        print(f"[GPT]     Retry {tentativa + 1}/{MAX_RETRIES}... ", end="", flush=True)
                    completion = client.chat.completions.create(
                        model=model,
                        messages=[
                            {"role": "system", "content": "Você é um especialista em análise de itens de licitação pública. Retorne APENAS o JSON conforme solicitado."},
                            {"role": "user", "content": prompt}
                        ],
                        max_tokens=16384,
                        temperature=0
                    )
                    resposta = completion.choices[0].message.content
                    print(f"OK ({len(resposta)} chars)")
                    break
                except Exception as e:
                    erros_total += 1
                    wait_time = 2 ** tentativa
                    print(f"ERRO!")
                    print(f"[GPT]       {type(e).__name__}: {e}")
                    if tentativa < MAX_RETRIES - 1:
                        print(f"[GPT]       Aguardando {wait_time}s...")
                        time.sleep(wait_time)

            if resposta:
                similares_chunk = _parse_resposta(resposta)
                if similares_chunk:
                    similaridades_totais.extend(similares_chunk)
                    print(f"[GPT]     → {len(similares_chunk)} similares encontrados neste chunk")
                elif resposta.strip() == "[]":
                    print(f"[GPT]     → 0 similares neste chunk")
                else:
                    print(f"[GPT]     ERRO parse. Primeiros 300 chars: {resposta[:300]}")
            else:
                print(f"[GPT]     FALHA: Sem resposta para chunk {chunk_idx + 1}")

            requisicoes_realizadas += 1

        print(f"[GPT]   TOTAL similares para este item: {len(similaridades_totais)}")

        resultado_estruturado = {
            "item_analisar": nome_item,
            "similaridade": similaridades_totais
        }
        resultado_itens.append(resultado_estruturado)

        # Salva progresso a cada item processado
        resultado_parcial = {
            "total_itens": total_itens,
            "total_selecionados": total_selecionados,
            "itens": resultado_itens
        }
        _salvar_progresso(resultado_parcial, OUTPUT_GPT)

        tempo_item = time.time() - tempo_inicio_item
        tempo_total_ate_agora = time.time() - tempo_inicio_total
        tempo_medio_por_item = tempo_total_ate_agora / (pos + 1)
        itens_restantes = total_selecionados - (pos + 1)
        tempo_estimado_restante = tempo_medio_por_item * itens_restantes

        print(f"[GPT]   Tempo do item: {tempo_item:.1f}s")
        print(f"[GPT]   Progresso salvo ({pos + 1}/{total_selecionados})")
        print(f"[GPT]   Tempo total: {tempo_total_ate_agora:.1f}s ({tempo_total_ate_agora/60:.1f}min)")
        print(f"[GPT]   Tempo médio/item: {tempo_medio_por_item:.1f}s | ETA: {tempo_estimado_restante:.0f}s ({tempo_estimado_restante/60:.1f}min)")

    tempo_total = time.time() - tempo_inicio_total
    print("\n" + "="*60)
    print(f"[GPT] CONCLUÍDO!")
    print(f"[GPT] Resultado salvo em: {OUTPUT_GPT}")
    print(f"[GPT] Tempo total: {tempo_total:.1f}s ({tempo_total/60:.1f}min)")
    print(f"[GPT] Requisições realizadas: {requisicoes_realizadas}")
    print(f"[GPT] Total erros API: {erros_total}")
    print("="*60)
    return resultado_itens


# ────────────────────────────── GEMINI ──────────────────────────────

def similaridade_gemini(api_key=None, model="gemini-2.0-flash"):
    """
    Seleciona 335 itens aleatórios de itens_complexos.json e compara cada um
    com TODOS os outros itens usando a API do Gemini, dividindo em chunks para
    evitar truncamento de resposta.
    Salva o resultado em json/array_similaridade_gemini_llm.json.
    
    Retorna apenas itens similares (similar=1) para cada item analisado.
    """
    print("="*60)
    print("[Gemini] Iniciando função similaridade_gemini")
    print(f"[Gemini] Modelo: {model}")
    print(f"[Gemini] Modo: chunks de {CHUNK_SIZE} itens por requisição (retorna só similares)")
    print("[Gemini] SDK: google-genai (novo)")
    print("="*60)

    if api_key is None:
        api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("API key do Gemini não fornecida. Defina GEMINI_API_KEY ou passe como parâmetro.")
    print("[Gemini] API key configurada com sucesso")

    print("[Gemini] Criando cliente Gemini (novo SDK)...")
    client = genai.Client(api_key=api_key)
    print("[Gemini] Cliente Gemini inicializado com sucesso")

    print("[Gemini] Carregando itens complexos do JSON...")
    itens = carregar_itens_complexos()

    if not itens:
        print("[Gemini] ERRO: Nenhum item encontrado. Abortando.")
        return []
    print(f"[Gemini] Itens carregados com sucesso: {len(itens)} itens")

    # Divide itens em chunks
    chunks = list(_chunkar_itens(itens, CHUNK_SIZE))
    total_chunks = len(chunks)
    print(f"[Gemini] Itens divididos em {total_chunks} chunks de até {CHUNK_SIZE} itens")

    print(f"[Gemini] Selecionando {SAMPLE_SIZE} itens aleatórios (seed={SEED})...")
    indices_selecionados = _selecionar_itens(itens)
    total_itens = len(itens)
    total_selecionados = len(indices_selecionados)
    total_requisicoes = total_selecionados * total_chunks
    print(f"[Gemini] Total de itens no dataset: {total_itens}")
    print(f"[Gemini] Total de itens selecionados: {total_selecionados}")
    print(f"[Gemini] Total de REQUISIÇÕES a fazer: {total_requisicoes} ({total_selecionados} itens × {total_chunks} chunks)")
    print(f"[Gemini] Índices selecionados (primeiros 10): {indices_selecionados[:10]}...")
    print(f"[Gemini] Arquivo de saída: {OUTPUT_GEMINI}")
    print("-"*60)

    resultado_itens = []
    tempo_inicio_total = time.time()
    requisicoes_realizadas = 0
    erros_total = 0

    for pos, i in enumerate(indices_selecionados):
        item_analisar = itens[i]
        nome_item = item_analisar.get("nome_item", "")
        classe_item = item_analisar.get("classe_item", "")
        tempo_inicio_item = time.time()
        
        print(f"\n[Gemini] ── Item {pos + 1}/{total_selecionados} (índice {i}) ──")
        print(f"[Gemini]   Nome: {nome_item}")
        print(f"[Gemini]   Classe: {classe_item}")

        similaridades_totais = []

        for chunk_idx, chunk in enumerate(chunks):
            chunk_json = json.dumps(chunk, ensure_ascii=False, indent=2)
            print(f"[Gemini]   Chunk {chunk_idx + 1}/{total_chunks} ({len(chunk)} itens, {len(chunk_json)} chars)... ", end="", flush=True)

            prompt = PROMPT_TEMPLATE.format(
                item_analisar=json.dumps(item_analisar, ensure_ascii=False),
                lista_itens_json=chunk_json
            )

            resposta = None
            for tentativa in range(MAX_RETRIES):
                try:
                    if tentativa > 0:
                        print(f"[Gemini]     Retry {tentativa + 1}/{MAX_RETRIES}... ", end="", flush=True)
                    response = client.models.generate_content(
                        model=model,
                        contents=prompt,
                        config=types.GenerateContentConfig(
                            max_output_tokens=65536,
                            temperature=0.0,
                        )
                    )
                    resposta = response.text
                    print(f"OK ({len(resposta)} chars)")
                    break
                except Exception as e:
                    erros_total += 1
                    wait_time = 2 ** tentativa
                    print(f"ERRO!")
                    print(f"[Gemini]       {type(e).__name__}: {e}")
                    if tentativa < MAX_RETRIES - 1:
                        print(f"[Gemini]       Aguardando {wait_time}s...")
                        time.sleep(wait_time)

            if resposta:
                similares_chunk = _parse_resposta(resposta)
                if similares_chunk:
                    similaridades_totais.extend(similares_chunk)
                    print(f"[Gemini]     → {len(similares_chunk)} similares encontrados neste chunk")
                elif resposta.strip() == "[]":
                    print(f"[Gemini]     → 0 similares neste chunk")
                else:
                    print(f"[Gemini]     ERRO parse. Primeiros 300 chars: {resposta[:300]}")
            else:
                print(f"[Gemini]     FALHA: Sem resposta para chunk {chunk_idx + 1}")

            requisicoes_realizadas += 1

        print(f"[Gemini]   TOTAL similares para este item: {len(similaridades_totais)}")

        resultado_estruturado = {
            "item_analisar": nome_item,
            "similaridade": similaridades_totais
        }
        resultado_itens.append(resultado_estruturado)

        # Salva progresso a cada item processado
        resultado_parcial = {
            "total_itens": total_itens,
            "total_selecionados": total_selecionados,
            "itens": resultado_itens
        }
        _salvar_progresso(resultado_parcial, OUTPUT_GEMINI)

        tempo_item = time.time() - tempo_inicio_item
        tempo_total_ate_agora = time.time() - tempo_inicio_total
        tempo_medio_por_item = tempo_total_ate_agora / (pos + 1)
        itens_restantes = total_selecionados - (pos + 1)
        tempo_estimado_restante = tempo_medio_por_item * itens_restantes

        print(f"[Gemini]   Tempo do item: {tempo_item:.1f}s")
        print(f"[Gemini]   Progresso salvo ({pos + 1}/{total_selecionados})")
        print(f"[Gemini]   Tempo total: {tempo_total_ate_agora:.1f}s ({tempo_total_ate_agora/60:.1f}min)")
        print(f"[Gemini]   Tempo médio/item: {tempo_medio_por_item:.1f}s | ETA: {tempo_estimado_restante:.0f}s ({tempo_estimado_restante/60:.1f}min)")

    tempo_total = time.time() - tempo_inicio_total
    print("\n" + "="*60)
    print(f"[Gemini] CONCLUÍDO!")
    print(f"[Gemini] Resultado salvo em: {OUTPUT_GEMINI}")
    print(f"[Gemini] Tempo total: {tempo_total:.1f}s ({tempo_total/60:.1f}min)")
    print(f"[Gemini] Requisições realizadas: {requisicoes_realizadas}")
    print(f"[Gemini] Total erros API: {erros_total}")
    print("="*60)
    return resultado_itens


# ────────────────────────────── MAIN ──────────────────────────────

if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Uso: python comparacaoLlm.py [gpt|gemini|ambos]")
        sys.exit(1)

    modo = sys.argv[1].lower()

    if modo in ("gpt", "ambos"):
        similaridade_gpt()
    if modo in ("gemini", "ambos"):
        similaridade_gemini()
    if modo not in ("gpt", "gemini", "ambos"):
        print(f"Modo '{modo}' não reconhecido. Use: gpt, gemini ou ambos")
