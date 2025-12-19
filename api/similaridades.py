import json
import kagglehub
from sentence_transformers import SentenceTransformer
import pickle
import os

# networkx é opcional — se não estiver instalado, usamos uma representação simples de grafo
try:
    import networkx as nx
    _HAS_NETWORKX = True
except Exception:
    nx = None
    _HAS_NETWORKX = False

def _load_items_from_json(path="itens.json"):
    """Carrega itens do arquivo JSON `itens.json`.

    O arquivo é esperado no formato em que `requisicaoApi.request` grava: cada linha
    contém um array JSON com vários objetos de item (apêndice). Retorna uma lista de dicts.
    """
    items = []
    if not path or not os.path.exists(path):
        return items

    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = f.read()
    except Exception:
        return items

    decoder = json.JSONDecoder()
    idx = 0
    length = len(data)
    while True:
        # pula espaços em branco
        while idx < length and data[idx].isspace():
            idx += 1
        if idx >= length:
            break
        try:
            obj, end = decoder.raw_decode(data, idx)
        except json.JSONDecodeError:
            # Se não for possível decodificar mais, interrompe
            break
        idx = end
        if isinstance(obj, list):
            items.extend(obj)
        else:
            items.append(obj)

    return items


def similaridades(items_source, similaridade_min, salvar_json=False):
    """
    Calcula similaridades. `items_source` pode ser:
      - caminho para arquivo JSON (ex: 'itens.json') => os itens serão lidos do arquivo
      - lista em memória (mantido para compatibilidade)
    """
    # Se não for passado, carrega do arquivo
    if (items_source == None):
        items = _load_items_from_json()
    else:
        items = items_source

    kagglehub.login() # This will prompt you for your credentials.

    # Define e carrega o modelo de embeddings
    MODEL_PATH = kagglehub.model_download("google/embeddinggemma/transformers/embeddinggemma-300m")
    model = SentenceTransformer(MODEL_PATH)
    
    descricao = []
    orgaos = []
    for item in items:
        # suporta dicts e objetos
        desc = item.get('descricao_item') if isinstance(item, dict) else getattr(item, 'descricao_item', None)
        org = item.get('nomeUnidade') if isinstance(item, dict) else getattr(item, 'nomeUnidade', None)
        if desc:
            descricao.append(desc)
            orgaos.append(org)
    
    if not descricao:
        return []

    # Gera embeddings para todas as descrições
    embeddings = model.encode(descricao, show_progress_bar=True)
    
    # Cria matriz de similaridade
    matrizSimilaridade = []
    
    for i in range(len(embeddings)):
        linha = {
            "linha": i,
            "descricao": descricao[i],
            "orgao": orgaos[i],
            "similaridades": []
        }
        
        for j in range(len(embeddings)):
            # Verifica se os orgãos são distintos
            if (orgaos[i] != orgaos[j] and descricao[i] != descricao[j]):
                # Calcula similaridade de cosseno entre os embeddings
                similaridade = float(model.similarity(embeddings[i], embeddings[j]))
                if (similaridade > similaridade_min):
                    linha["similaridades"].append({
                        "Coluna": j,
                        "descricao": descricao[j],
                        "orgao": orgaos[j],
                        "similaridade": similaridade
                    })
        if (linha["similaridades"] != []):
            matrizSimilaridade.append(linha)

    if (salvar_json):
        # Salva a matriz em formato JSON num arquivo legível
        with open(f"matriz_Similaridade_{int(similaridade_min * 100)}_porcento.json", "w", encoding="utf-8") as f:
            json.dump(matrizSimilaridade, f, ensure_ascii=False, indent=2)

        print(f"Matriz de Similaridade Calculada e salva no arquivo: matriz_Similaridade_{int(similaridade_min * 100)}_porcento.json")


def similaridadesGrafo(items_list, similaridade_min, salvar_arquivo=False, arquivo_saida=None):
    """
    Constrói um grafo de similaridades entre itens.

    - Nós: cada item que possui `descricao_item` (mantemos o índice original do `items_list` como id do nó)
    - Arestas: entre nós de órgãos distintos cuja similaridade de cosseno é > similaridade_min

    Se `networkx` estiver disponível, retorna um objeto networkx.Graph com atributos:
      node attrs: descricao, orgao, idx_in_list
      edge attr: weight (similaridade)

    Se `networkx` não estiver disponível, retorna um dicionário com chaves "nodes" e "edges".

    Parâmetros:
      items_list: lista de objetos com atributos `descricao_item` e `nomeUnidade`
      similaridade_min: float (0..1) limiar para criar arestas
      salvar_arquivo: bool - se True salva o grafo em disco
      arquivo_saida: caminho/filename opcional (sem extensão é adicionado automaticamente)

    Retorna:
      Grafo (networkx.Graph ou dict)
    """
    # Se receber um caminho para o arquivo, carrega os itens do JSON
    if (items_list == None):
        print("carregando itens do arquivo JSON...")
        items_list = _load_items_from_json()
    else:
        print("usando itens fornecidos em memória...")
        items_list = items_list

    # autenticação e carregamento de modelo (mesma lógica da função original)
    kagglehub.login()
    print("carregando modelo de embeddings...")

    MODEL_PATH = kagglehub.model_download("google/embeddinggemma/transformers/embeddinggemma-300m")
    model = SentenceTransformer(MODEL_PATH)
    print("modelo carregado.")

    # Recolhe descrições, órgãos, datas e índice original para mapear nós
    descricao = []
    orgaos = []
    datas = []
    original_idx = []
    for idx, item in enumerate(items_list):
        # suporta dicts e objetos
        desc = item.get('descricao_item') if isinstance(item, dict) else getattr(item, 'descricao_item', None)
        org = item.get('nomeUnidade') if isinstance(item, dict) else getattr(item, 'nomeUnidade', None)
        data = item.get('data_desejada') if isinstance(item, dict) else getattr(item, 'data_desejada', None)
        if desc:
            descricao.append(desc)
            orgaos.append(org)
            datas.append(data)
            original_idx.append(idx)
    print(f"Total de itens com descrição: {len(descricao)}")

    # Se não houver descrições suficientes, retorna grafo vazio
    if len(descricao) == 0:
        if _HAS_NETWORKX:
            return nx.Graph()
        return {"nodes": [], "edges": []}

    embeddings = model.encode(descricao, show_progress_bar=True)
    print("embeddings gerados.")

    # Cria grafo
    print("construindo grafo de similaridades...")
    if _HAS_NETWORKX:
        G = nx.Graph()
        for i in range(len(descricao)):
            G.add_node(original_idx[i], descricao=descricao[i], orgao=orgaos[i], data=datas[i], idx_in_list=i)
    else:
        G = {"nodes": [], "edges": []}
        for i in range(len(descricao)):
            G["nodes"].append({
                "id": original_idx[i],
                "descricao": descricao[i],
                "orgao": orgaos[i],
                "data": datas[i],
                "idx_in_list": i
            })
    print("nós adicionados ao grafo.")
    
    # Calcula similaridades e adiciona arestas (somente uma vez por par i<j)
    print("adicionando arestas ao grafo...")
    contador = 0
    for i in range(len(embeddings)):
        print(f"Processando nó {i+1} de {len(embeddings)}...")
        for j in range(i + 1, len(embeddings)):
            # Verifica se os órgãos são distintos
            if (orgaos[i] != orgaos[j]):
                similaridade = float(model.similarity(embeddings[i], embeddings[j]))
                if (similaridade > similaridade_min):
                    contador += 2
                    if _HAS_NETWORKX:
                        G.add_edge(original_idx[i], original_idx[j], weight=similaridade)
                    else:
                        G["edges"].append({
                            "source": original_idx[i],
                            "target": original_idx[j],
                            "similaridade": similaridade
                        })

    # Salva em arquivo se solicitado
    print("grafo construído.")
    if salvar_arquivo:
        if arquivo_saida is None:
            arquivo_saida = f"grafo_Similaridade_{int(similaridade_min * 100)}_porcento"

        if _HAS_NETWORKX:
            # Salva como gpickle por ser simples e preservar atributos
            path = arquivo_saida if arquivo_saida.endswith('.gpickle') else arquivo_saida + '.gpickle'
            # Compatibilidade com várias versões do networkx:
            try:
                # networkx <= 2.x may expose write_gpickle at top-level
                if hasattr(nx, 'write_gpickle'):
                    nx.write_gpickle(G, path)
                else:
                    # newer networkx exposes gpickle under readwrite
                    nx.readwrite.gpickle.write_gpickle(G, path)
                print(f"Grafo salvo em: {path} (formato: gpickle)")
            except Exception:
                # Fallback simples: gravar com pickle (compatível para carregamento local)
                with open(path, 'wb') as f:
                    pickle.dump(G, f)
                print(f"Grafo salvo em: {path} usando pickle como fallback")
        else:
            # Salva estrutura alternativa em JSON
            path = arquivo_saida if arquivo_saida.endswith('.json') else arquivo_saida + '.json'
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(G, f, ensure_ascii=False, indent=2)
            print(f"Grafo (representação JSON) salvo em: {path}")

    print(f"Total de arestas: {contador // 2}, Contador: {contador}")
    return contador