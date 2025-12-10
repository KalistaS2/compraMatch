from similaridades import similaridades, similaridadesGrafo
from requisicaoApi import request

def main():

    # Create an empty list to store items
    # items_list = request(anoPca="2024", max_items=10000, tamanhoPagina="90", url="https://pncp.gov.br/api/consulta/v1/pca/", minPagina=1, maxPagina=5)

    # Ate aqui foi feito a gravação dos itens em cache e nos arquivos JSON.
    # a partir daqui tera a construção da matriz e operação de similaridade de todos com todos.

    #similaridades(None, similaridade_min=0.9, salvar_json=True)
    similaridadesGrafo(items_list = None, similaridade_min = 0.7, salvar_arquivo=True, arquivo_saida="grafo_similaridades")

if __name__ == "__main__":
    main()
