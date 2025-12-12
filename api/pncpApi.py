import os
import sys

# Adiciona o diretório 'api' ao caminho para importações
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from similaridades import similaridades, similaridadesGrafo
from requisicaoApi import request
from orgaos import extrair_orgaos
from app import app

def main():

    # Create an empty list to store items
    # request(anoPca="2024", max_items=10000, tamanhoPagina="90", url="https://pncp.gov.br/api/consulta/v1/pca/", minPagina=1, maxPagina=5)

    # Ate aqui foi feito a gravação dos itens em cache e nos arquivos JSON.
    # a partir daqui tera a construção da matriz e operação de similaridade de todos com todos.
    # similaridadesGrafo(items_list = None, similaridade_min=0.9, salvar_arquivo=True)
    """Executa a aplicação web Flask."""
    
    # Informações da aplicação
    
    print("=" * 60)
    print("CompraJunto - Sistema de Compras Compartilhadas")
    print("=" * 60)
    
    # Carrega informações dos órgãos
    lista_orgaos = extrair_orgaos("../itens.json")
    print(f"\n✓ Total de órgãos carregados: {len(lista_orgaos)}")
    
    # Inicia servidor Flask
    print("\n🚀 Iniciando servidor web...")
    print("📱 Acesse: http://127.0.0.1:5000")
    print("⚠️  Pressione CTRL+C para parar o servidor\n")
    
    # Executa a aplicação web
    app.run(debug=True, host='127.0.0.1', port=5000, use_reloader=False)

if __name__ == "__main__":
    main()
