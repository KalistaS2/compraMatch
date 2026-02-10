import kagglehub
import json
from sentence_transformers import SentenceTransformer
from construcao import carregar_itens_complexos


def similaridades_baseline(similaridade_min=0.7, salvar_json=True):
    """
    Calcula similaridades usando Gemma Embeddings. `items_source` pode ser:
      - None => os itens serão carregados de itens_complexos.json usando carregar_itens_complexos()
      - lista em memória (mantido para compatibilidade)
    """
    # Se não for passado, carrega usando carregar_itens_complexos
    items = carregar_itens_complexos()

    if not items:
        print("Nenhum item encontrado para processar")
        return []

    kagglehub.login() # This will prompt you for your credentials.

    # Define e carrega o modelo de embeddings
    MODEL_PATH = kagglehub.model_download("google/embeddinggemma/transformers/embeddinggemma-300m")
    model = SentenceTransformer(MODEL_PATH)
    
    descricao = []
    classe = []
    for item in items:
        # suporta dicts e objetos
        desc = item.get('nome_item') if isinstance(item, dict) else getattr(item, 'nome_item', None)
        cl = item.get('classe_item') if isinstance(item, dict) else getattr(item, 'classe_item', None)
        if desc:
            descricao.append(desc)
            classe.append(cl)
    
    if not descricao:
        print("Nenhuma descrição de item encontrada")
        return []

    print(f"Gerando embeddings para {len(descricao)} itens...")
    # Gera embeddings para todas as descrições
    embeddings = model.encode(descricao, show_progress_bar=True)
    print("Embeddings gerados.")
    
    # Cria array de similaridades na mesma estrutura de processar_itens
    resultado_itens = []
    
    for i in range(len(embeddings)):
        print(f"Processando item {i+1} de {len(embeddings)}...")
        
        # Array de comparações deste item com todos os outros
        similaridades_item = []
        
        for j in range(len(embeddings)):
            # Verifica se as descrições são distintas
            # Calcula similaridade de cosseno entre os embeddings
            similaridade = float(model.similarity(embeddings[i], embeddings[j]))
            
            similaridades_item.append({
                'indice': j,
                'item': descricao[j],
                'classe': classe[j],
                'similaridade': similaridade
            })
        
        # Adiciona item com suas similaridades
        resultado_itens.append({
            'indice': i,
            'item': descricao[i],
            'classe': classe[i],
            'similaridade': similaridades_item
        })

    if salvar_json:
        # Salva o array em formato JSON num arquivo legível
        resultado = {
            'total_itens': len(descricao),
            'itens': resultado_itens
        }
        
        with open(f"../json/array_similaridade_gemma_{int(similaridade_min * 100)}_porcento.json", "w", encoding="utf-8") as f:
            json.dump(resultado, f, ensure_ascii=False, indent=2)

        print(f"Array de Similaridade Gemma Calculado e salvo no arquivo: json/array_similaridade_gemma_{int(similaridade_min * 100)}_porcento.json")
    
    return resultado_itens
