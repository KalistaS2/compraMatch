import requests
import json
from datetime import datetime, date
from model.items import PcaItem
import kagglehub
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

def main():

    # Create an empty list to store items
    items_list = []
        
    # URL da API PNCP CONSULTA
    url = "https://pncp.gov.br/api/consulta/v1/pca/"

    for pagina in range(1, 5):
        for cod in range(1, 50):
            # Parâmetros aceitos pela API
            params = {
                "anoPca": "2024",
                "codigoClassificacaoSuperior": cod,
                "pagina": pagina,
                "tamanhoPagina": "90"
            }
            headers = {"accept": "*/*"}

            response = requests.get(url, headers=headers, params=params)

            if response.status_code == 200:
                data = response.json()


                for pca in data.get("data", []):
                    for item in pca.get("itens", []):
                        # Conversões seguras de data/hora
                        data_inclusao = datetime.fromisoformat(item["dataInclusao"]) if item.get("dataInclusao") else None
                        data_atualizacao = datetime.fromisoformat(item["dataAtualizacao"]) if item.get("dataAtualizacao") else None
                        data_desejada = date.fromisoformat(item["dataDesejada"]) if item.get("dataDesejada") else None

                        # Criação do objeto PcaItem com todos os parâmetros se for Material
                        if (item.get("nomeClassificacaoCatalogo") == "Material"):
                            pca_item = PcaItem(
                                descricao_item=item.get("descricaoItem"),
                                nome_classificacao_catalogo=item.get("nomeClassificacaoCatalogo"),
                                quantidade_estimada=item.get("quantidadeEstimada", 0),
                                pdm_codigo=item.get("pdmCodigo"),
                                data_inclusao=data_inclusao,
                                numero_item=item.get("numeroItem", 0),
                                data_atualizacao=data_atualizacao,
                                valor_total=item.get("valorTotal", 0),
                                pdm_descricao=item.get("pdmDescricao"),
                                codigo_item=item.get("codigoItem"),
                                unidade_requisitante=item.get("unidadeRequisitante"),
                                grupo_contratacao_codigo=item.get("grupoContratacaoCodigo"),
                                grupo_contratacao_nome=item.get("grupoContratacaoNome"),
                                classificacao_superior_codigo=item.get("classificacaoSuperiorCodigo"),
                                classificacao_superior_nome=item.get("classificacaoSuperiorNome"),
                                unidade_fornecimento=item.get("unidadeFornecimento"),
                                valor_unitario=item.get("valorUnitario", 0),
                                valor_orcamento_exercicio=item.get("valorOrcamentoExercicio", 0),
                                data_desejada=data_desejada,
                                categoria_item_pca_nome=item.get("categoriaItemPcaNome"),
                                classificacao_catalogo_id=item.get("classificacaoCatalogoId", 0),
                                nomeUnidade=pca.get("nomeUnidade")
                            )
                            items_list.append(pca_item)

                # Registra os itens resgatados no arquivo itens.json
                with open("itens.json", "a", encoding="utf-8") as f:
                    json.dump(
                        [item.__dict__ for item in items_list],
                        f,
                        ensure_ascii=False,
                        indent=2,
                        default=str  # converte datetime/date para string
                    )
                    f.write("\n")

                # Optionally, save to a local file (JSON)
                with open("pncp_response.json", "a", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=4)

                print("✅ Response saved to pncp_response.json")

                print(f"Created {len(items_list)} PCA Items.")
            else:
                print(f"❌ Failed to get data: {response.status_code}")
            if (len(items_list) >= 1000):
                pagina = 10
                break
        if (len(items_list) >= 1000):
            pagina = 10
            break

    # Ate aqui foi feito a gravação dos itens em cache e nos arquivos JSON.
    # a partir daqui tera a construção da matriz e operação de similaridade de todos com todos.
    
    # Authenticate
    kagglehub.login() # This will prompt you for your credentials.

    MODEL_PATH = kagglehub.model_download("google/embeddinggemma/transformers/embeddinggemma-300m")
    model = SentenceTransformer(MODEL_PATH)
    
    # Cria vetores de documentos baseados na descrição dos itens
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
                if (similaridade > 0.9):
                    linha["similaridades"].append({
                        "Coluna": j,
                        "descricao": descricao[j],
                        "orgao": orgaos[j],
                        "similaridade": similaridade
                    })
        if (linha["similaridades"] != []):
            matrizSimilaridade.append(linha)

    # Salva a matriz em formato JSON num arquivo legível
    with open("matriz_Similaridade_90_porcento.json", "w", encoding="utf-8") as f:
        json.dump(matrizSimilaridade, f, ensure_ascii=False, indent=2)

    print("Matriz de Similaridade Calculada e salva no arquivo: matriz_Similaridade.json")

if __name__ == "__main__":
    main()
