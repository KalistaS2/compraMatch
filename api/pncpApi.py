import spacy
import pt_core_news_sm
import requests
import json
from datetime import datetime, date
from model.items import PcaItem
def main():

    # URL da API PNCP CONSULTA
    url = "https://pncp.gov.br/api/consulta/v1/pca/"

    # Parâmetros aceitos pela API
    params = {
        "anoPca": "2024",
        "codigoClassificacaoSuperior": "2",
        "pagina": "1",
        "tamanhoPagina": "90"
    }
    headers = {"accept": "*/*"}

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()

        # Create an empty list to store items
        items_list = []

        for pca in data.get("data", []):
            for item in pca.get("itens", []):
                # Conversões seguras de data/hora
                data_inclusao = datetime.fromisoformat(item["dataInclusao"]) if item.get("dataInclusao") else None
                data_atualizacao = datetime.fromisoformat(item["dataAtualizacao"]) if item.get("dataAtualizacao") else None
                data_desejada = date.fromisoformat(item["dataDesejada"]) if item.get("dataDesejada") else None

                # Criação do objeto PcaItem com todos os parâmetros
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

                if item.get("descricaoItem"):
                    print(
                        f"Item: {item.get('descricaoItem')}, "
                        f"Órgão: {item.get('unidadeRequisitante')}, "
                        f"Nome Unidade: {pca.get('nomeUnidade')}"
                    )

        with open("itens.json", "w", encoding="utf-8") as f:
            json.dump(
                [item.__dict__ for item in items_list],
                f,
                ensure_ascii=False,
                indent=2,
                default=str  # converte datetime/date para string
            )
            f.write("\n")

        # Optionally, save to a local file (JSON)
        with open("pncp_response.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        print("✅ Response saved to pncp_response.json")
        
        print(f"Created {len(items_list)} PCA Items.")
    else:
        print(f"❌ Failed to get data: {response.status_code}")
        
    # Ate aqui foi feito a gravação dos itens em cache e nos arquivos JSON.
    # a partir daqui tera a construção da matriz e operação de similaridade de todos com todos.

    # Carrega modelo spaCy para português
    nlp = spacy.load("pt_core_news_sm")

    # Cria vetores de documentos baseados na descrição dos itens
    descricao = [item.descricao_item for item in items_list]
    itensNlp = [nlp(desc) for desc in descricao]

    # Cria matriz de similaridade
    matrizSimilaridade = []
    for i, doc1 in enumerate(itensNlp):
        linha = []
        for j, doc2 in enumerate(itensNlp):
            similaridade = doc1.similarity(doc2)
            linha.append(similaridade)
        matrizSimilaridade.append(linha)
    print("Matriz de Similaridade Calculada:")
    for linha in matrizSimilaridade:
        print(linha)

if __name__ == "__main__":
    main()
