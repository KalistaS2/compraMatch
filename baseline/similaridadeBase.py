"""
Módulo de cálculo de similaridades para a baseline sintética.
Utiliza o modelo de embeddings para calcular similaridades entre itens.
"""

import sys
import json
from pathlib import Path

# Adiciona o diretório api ao path para importar similaridades
sys.path.insert(0, str(Path(__file__).parent.parent / "api"))

from similaridades import similaridadesGrafo



def calcular_similaridades_baseline(caminho_itens="itensSinteticos.json", 
                                   similaridade_min=0.7, 
                                   salvar_grafo=True):
    """
    Calcula as similaridades entre os itens sintéticos usando a função similaridadesGrafo.
    
    Args:
        caminho_itens: caminho para o arquivo JSON com os itens
        similaridade_min: limiar mínimo de similaridade (0-1)
        salvar_grafo: se True, salva o grafo em arquivo
        
    Retorna:
        tuple: (grafo, caminho_arquivo_grafo)
    """
    print("=" * 60)
    print("CÁLCULO DE SIMILARIDADES BASELINE")
    print("=" * 60)
    
    # Resolve caminho absoluto
    arquivo_itens = Path(__file__).parent / caminho_itens
    
    if not arquivo_itens.exists():
        print(f"✗ Arquivo não encontrado: {arquivo_itens}")
        print("Execute construcao.py primeiro para gerar os itens sintéticos.")
        return None, None
    
    # Carrega itens do JSON
    print(f"\nCarregando itens de: {arquivo_itens}")
    with open(arquivo_itens, 'r', encoding='utf-8') as f:
        itens = json.load(f)
    
    print(f"✓ {len(itens)} itens carregados")
    
    # Calcula similaridades usando o grafo
    print(f"\nCalculando grafo de similaridades (limiar: {similaridade_min})...")
    print("Isso pode levar alguns minutos dependendo da quantidade de itens...")
    
    try:
        resultado = similaridadesGrafo(
            items_list=itens,
            similaridade_min=similaridade_min,
            salvar_arquivo=salvar_grafo,
            arquivo_saida=f"grafo_Similaridade_{int(similaridade_min * 100)}_porcento"
        )
        
        print(f"\n✓ Grafo de similaridades calculado com sucesso!")
        print(f"✓ Total de pares similares: {resultado // 2}")
        
        # Define caminho do grafo
        arquivo_grafo = Path(__file__).parent / f"grafo_Similaridade_{int(similaridade_min * 100)}_porcento.gpickle"
        
        return resultado, str(arquivo_grafo)
        
    except Exception as e:
        print(f"✗ Erro ao calcular similaridades: {e}")
        import traceback
        traceback.print_exc()
        return None, None


def main():
    """Função principal."""
    resultado = calcular_similaridades_baseline(
        caminho_itens="itensSinteticos.json",
        similaridade_min=0.7,
        salvar_grafo=True
    )
    
    if resultado[0] is not None:
        print("\n" + "=" * 60)
        print("SIMILARIDADES CALCULADAS COM SUCESSO!")
        print("=" * 60)
    else:
        print("\nFalha ao calcular similaridades.")
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
