import json
import kagglehub
from sentence_transformers import SentenceTransformer

def similaridades(items_list, similaridade_min, salvar_json=False):
    kagglehub.login() # This will prompt you for your credentials.

    # Define e carrega o modelo de embeddings
    MODEL_PATH = kagglehub.model_download("google/embeddinggemma/transformers/embeddinggemma-300m")
    model = SentenceTransformer(MODEL_PATH)
    
    descricao = []
    for item in items_list:
        if (item.descricao_item):
            descricao.append(item.descricao_item)
    
    # Gera embeddings para todas as descrições
    embeddings = model.encode(descricao, show_progress_bar=True)

    # Cria uma lista com os orgãos para fazer a similaridade de itens em diversos PCAs
    orgaos = [item.nomeUnidade for item in items_list]
    
    # Cria matriz de similaridade
    # Cada entrada contém o índice, a descrição do documento e uma lista de similaridades
    matrizSimilaridade = []
    
    for i in range(len(embeddings)):
        
        #cria a variavel que recebe a string que vai aplicar a similaridade e reseta toda vez que mudar a linha
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