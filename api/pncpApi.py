import os
import sys
import requests
import json


def main():
    # Ensure project root is on sys.path so `import api.settings` works when running this file directly
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if project_root not in sys.path:
        sys.path.insert(0, project_root)

    # Initialize Django settings so models can be imported when running this script directly
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "api.settings")  # adjust if your settings module path is different
    import django
    django.setup()

    from model.items import PcaItem
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
                # Create PcaItem object and add to the list
                pca_item = PcaItem.objects.create(
                    descricao_item=item.get("descricaoItem"),
                    nome_classificacao_catalogo=item.get("nomeClassificacaoCatalogo"),
                    quantidade_estimada=item.get("quantidadeEstimada", 0),
                    valor_total=item.get("valorTotal", 0),
                    unidade_requisitante=item.get("unidadeRequisitante"),
                    data_inclusao=item.get("dataInclusao"),
                    data_atualizacao=item.get("dataAtualizacao"),
                    data_desejada=item.get("dataDesejada"),
                    nome_unidade=pca.get("nomeUnidade")
                )
                items_list.append(pca_item)
                if item.get("descricaoItem"):
                    print(f"Item: {item.get('descricaoItem')}, orgao: {item.get('unidadeRequisitante')}, nomeUnidade: {pca.get('nomeUnidade')}")

        with open("lista_Itens.json", "w", encoding="utf-8") as f:
            for item in items_list:
                json.dump(item.__dict__, f, ensure_ascii=False)
                f.write("\n")

        # Optionally, save to a local file (JSON)
        with open("pncp_response.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

        print("✅ Response saved to pncp_response.json")
        print(f"Created {len(items_list)} PCA Items.")
    else:
        print(f"❌ Failed to get data: {response.status_code}")


if __name__ == "__main__":
    main()
