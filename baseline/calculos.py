"""
Módulo de cálculo de métricas de qualidade para a baseline sintética.
Calcula: Precisão, Acurácia, Erro Absoluto Médio (MAE), RMSE e outras métricas.
"""

import json
import math
from pathlib import Path
from itertools import combinations


def carregar_itens(caminho="itensSinteticos.json"):
    """
    Carrega os itens sintéticos do arquivo JSON.
    
    Args:
        caminho: caminho para o arquivo JSON
        
    Retorna:
        list: Lista de itens
    """
    arquivo = Path(__file__).parent / caminho
    
    if not arquivo.exists():
        print(f"✗ Arquivo não encontrado: {arquivo}")
        return None
    
    with open(arquivo, 'r', encoding='utf-8') as f:
        return json.load(f)


def determinar_pares_esperados(itens):
    """
    Determina quais pares de itens DEVERIAM ser similares na baseline.
    
    Na baseline sintética, dois itens são considerados similares esperados se:
    - Pertencem a empresas (órgãos) diferentes
    - Compartilham pelo menos 2 características (tipo, cor, formato)
    
    Args:
        itens: lista de itens sintéticos
        
    Retorna:
        set: Conjunto de tuplas (idx_i, idx_j) com pares esperados como similares
    """
    pares_esperados = set()
    
    for i, j in combinations(range(len(itens)), 2):
        item_i = itens[i]
        item_j = itens[j]
        
        # Verifica se são de empresas diferentes
        if item_i["empresa"] == item_j["empresa"]:
            continue
        
        # Conta características em comum
        caracteristicas_comuns = 0
        if item_i["tipo"] == item_j["tipo"]:
            caracteristicas_comuns += 1
        if item_i["cor"] == item_j["cor"]:
            caracteristicas_comuns += 1
        if item_i["formato"] == item_j["formato"]:
            caracteristicas_comuns += 1
        
        # Se compartilha pelo menos 2 características, é similar esperado
        if caracteristicas_comuns >= 2:
            pares_esperados.add((i, j))
    
    return pares_esperados


def determinar_pares_detectados(grafo_resultado, caminho_grafo="grafo_Similaridade_70_porcento.gpickle"):
    """
    Carrega os pares detectados como similares pelo modelo.
    
    Args:
        grafo_resultado: resultado da função similaridadesGrafo (número de arestas)
        caminho_grafo: caminho para o arquivo do grafo
        
    Retorna:
        set: Conjunto de tuplas (idx_i, idx_j) com pares detectados como similares
    """
    pares_detectados = set()
    
    arquivo_grafo = Path(__file__).parent / caminho_grafo
    
    if not arquivo_grafo.exists():
        print(f"⚠ Arquivo de grafo não encontrado: {arquivo_grafo}")
        print("  Retornando conjunto vazio de pares detectados")
        return pares_detectados
    
    try:
        import pickle
        import networkx as nx
        
        with open(arquivo_grafo, 'rb') as f:
            grafo = pickle.load(f)
        
        # Se é um grafo networkx
        if isinstance(grafo, nx.Graph):
            for edge in grafo.edges():
                idx_i, idx_j = edge
                # Normaliza para (menor, maior) para compatibilidade
                pares_detectados.add((min(idx_i, idx_j), max(idx_i, idx_j)))
        # Se é um dicionário
        elif isinstance(grafo, dict) and "edges" in grafo:
            for edge in grafo["edges"]:
                idx_i = edge["source"]
                idx_j = edge["target"]
                pares_detectados.add((min(idx_i, idx_j), max(idx_i, idx_j)))
    
    except Exception as e:
        print(f"⚠ Erro ao carregar grafo: {e}")
        print("  Será necessário recalcular as similaridades")
        return pares_detectados
    
    return pares_detectados


def calcular_metricas(pares_esperados, pares_detectados, total_pares):
    """
    Calcula as métricas de qualidade baseadas nos pares.
    
    Args:
        pares_esperados: set de pares que deveriam ser similares
        pares_detectados: set de pares detectados como similares
        total_pares: número total de pares possíveis
        
    Retorna:
        dict: Dicionário com as métricas calculadas
    """
    # True Positives: detectados e esperados
    tp = len(pares_esperados & pares_detectados)
    
    # False Positives: detectados mas não esperados
    fp = len(pares_detectados - pares_esperados)
    
    # False Negatives: esperados mas não detectados
    fn = len(pares_esperados - pares_detectados)
    
    # True Negatives: nem esperados nem detectados
    tn = total_pares - tp - fp - fn
    
    # Cálculos de métricas
    metricas = {
        "tp": tp,
        "fp": fp,
        "fn": fn,
        "tn": tn,
        "total_pares": total_pares,
        "pares_esperados": len(pares_esperados),
        "pares_detectados": len(pares_detectados),
    }
    
    # Precisão: TP / (TP + FP)
    if tp + fp > 0:
        metricas["precisao"] = tp / (tp + fp)
    else:
        metricas["precisao"] = 0.0
    
    # Recall (Sensibilidade): TP / (TP + FN)
    if tp + fn > 0:
        metricas["recall"] = tp / (tp + fn)
    else:
        metricas["recall"] = 0.0
    
    # Acurácia: (TP + TN) / Total
    metricas["acuracia"] = (tp + tn) / total_pares if total_pares > 0 else 0.0
    
    # F1-Score: 2 * (Precisão * Recall) / (Precisão + Recall)
    if metricas["precisao"] + metricas["recall"] > 0:
        metricas["f1_score"] = (
            2 * metricas["precisao"] * metricas["recall"] / 
            (metricas["precisao"] + metricas["recall"])
        )
    else:
        metricas["f1_score"] = 0.0
    
    # Especificidade: TN / (TN + FP)
    if tn + fp > 0:
        metricas["especificidade"] = tn / (tn + fp)
    else:
        metricas["especificidade"] = 0.0
    
    # Taxa de Falsos Positivos: FP / (FP + TN)
    if fp + tn > 0:
        metricas["taxa_fp"] = fp / (fp + tn)
    else:
        metricas["taxa_fp"] = 0.0
    
    # Taxa de Falsos Negativos: FN / (FN + TP)
    if fn + tp > 0:
        metricas["taxa_fn"] = fn / (fn + tp)
    else:
        metricas["taxa_fn"] = 0.0
    
    return metricas


def calcular_metricas_erro(pares_esperados, pares_detectados):
    """
    Calcula métricas de erro: MAE e RMSE.
    
    Interpretação:
    - Cada par esperado não detectado tem "erro" de 1
    - Cada par falso positivo tem "erro" de 1
    
    Args:
        pares_esperados: set de pares esperados
        pares_detectados: set de pares detectados
        
    Retorna:
        dict: Dicionário com MAE e RMSE
    """
    # Erros: união de (esperados não detectados) + (falsos positivos)
    erros_indices = (pares_esperados - pares_detectados) | (pares_detectados - pares_esperados)
    
    total_erros = len(erros_indices)
    total_comparacoes = len(pares_esperados) + len(pares_detectados - pares_esperados)
    
    metricas_erro = {}
    
    # MAE (Mean Absolute Error)
    if total_comparacoes > 0:
        metricas_erro["mae"] = total_erros / total_comparacoes
    else:
        metricas_erro["mae"] = 0.0
    
    # RMSE (Root Mean Square Error)
    # Considerando cada erro como 1
    if total_comparacoes > 0:
        metricas_erro["rmse"] = math.sqrt(total_erros / total_comparacoes)
    else:
        metricas_erro["rmse"] = 0.0
    
    metricas_erro["total_erros"] = total_erros
    metricas_erro["total_comparacoes"] = total_comparacoes
    
    return metricas_erro


def salvar_relatorio(metricas, metricas_erro, itens, caminho="relatorio_metricas.json"):
    """
    Salva um relatório completo das métricas em arquivo JSON.
    
    Args:
        metricas: dicionário com as métricas de classificação
        metricas_erro: dicionário com as métricas de erro
        itens: lista de itens (para estatísticas)
        caminho: caminho do arquivo de saída
    """
    relatorio = {
        "info": {
            "total_itens": len(itens),
            "tipos": len(set(item["tipo"] for item in itens)),
            "cores": len(set(item["cor"] for item in itens)),
            "formatos": len(set(item["formato"] for item in itens)),
            "empresas": len(set(item["empresa"] for item in itens)),
        },
        "metricas_classificacao": metricas,
        "metricas_erro": metricas_erro,
    }
    
    arquivo = Path(__file__).parent / caminho
    
    with open(arquivo, 'w', encoding='utf-8') as f:
        json.dump(relatorio, f, ensure_ascii=False, indent=2)
    
    print(f"\n✓ Relatório salvo em: {arquivo}")
    return str(arquivo)


def imprimir_relatorio(metricas, metricas_erro, itens):
    """
    Imprime um relatório formatado das métricas no console.
    """
    print("\n" + "=" * 60)
    print("RELATÓRIO DE MÉTRICAS - BASELINE SINTÉTICA")
    print("=" * 60)
    
    print("\n📊 INFORMAÇÕES DO DATASET:")
    print(f"  Total de itens: {len(itens)}")
    print(f"  Tipos de canetas: {len(set(item['tipo'] for item in itens))}")
    print(f"  Cores: {len(set(item['cor'] for item in itens))}")
    print(f"  Formatos: {len(set(item['formato'] for item in itens))}")
    print(f"  Empresas: {len(set(item['empresa'] for item in itens))}")
    
    print("\n📈 ESTATÍSTICAS DE PARES:")
    print(f"  Total de pares possíveis: {metricas['total_pares']}")
    print(f"  Pares esperados como similares: {metricas['pares_esperados']}")
    print(f"  Pares detectados como similares: {metricas['pares_detectados']}")
    
    print("\n✅ MATRIZ DE CONFUSÃO:")
    print(f"  True Positives (TP): {metricas['tp']}")
    print(f"  False Positives (FP): {metricas['fp']}")
    print(f"  False Negatives (FN): {metricas['fn']}")
    print(f"  True Negatives (TN): {metricas['tn']}")
    
    print("\n🎯 MÉTRICAS DE CLASSIFICAÇÃO:")
    print(f"  Precisão: {metricas['precisao']:.4f} ({metricas['precisao']*100:.2f}%)")
    print(f"  Recall (Sensibilidade): {metricas['recall']:.4f} ({metricas['recall']*100:.2f}%)")
    print(f"  Acurácia: {metricas['acuracia']:.4f} ({metricas['acuracia']*100:.2f}%)")
    print(f"  F1-Score: {metricas['f1_score']:.4f}")
    print(f"  Especificidade: {metricas['especificidade']:.4f} ({metricas['especificidade']*100:.2f}%)")
    print(f"  Taxa de Falsos Positivos: {metricas['taxa_fp']:.4f} ({metricas['taxa_fp']*100:.2f}%)")
    print(f"  Taxa de Falsos Negativos: {metricas['taxa_fn']:.4f} ({metricas['taxa_fn']*100:.2f}%)")
    
    print("\n❌ MÉTRICAS DE ERRO:")
    print(f"  MAE (Erro Absoluto Médio): {metricas_erro['mae']:.4f}")
    print(f"  RMSE (Raiz do Erro Quadrático Médio): {metricas_erro['rmse']:.4f}")
    print(f"  Total de erros: {metricas_erro['total_erros']} / {metricas_erro['total_comparacoes']}")
    
    print("\n" + "=" * 60)


def main():
    """Função principal para calcular e exibir métricas."""
    print("=" * 60)
    print("CÁLCULO DE MÉTRICAS - BASELINE SINTÉTICA")
    print("=" * 60)
    
    # Carrega itens
    print("\nCarregando itens sintéticos...")
    itens = carregar_itens()
    if itens is None:
        print("✗ Falha ao carregar itens. Execute construcao.py primeiro.")
        return 1
    print(f"✓ {len(itens)} itens carregados")
    
    # Determina pares esperados
    print("\nDeterminando pares esperados como similares...")
    pares_esperados = determinar_pares_esperados(itens)
    print(f"✓ {len(pares_esperados)} pares esperados como similares")
    
    # Determina pares detectados
    print("\nCarregando pares detectados como similares...")
    pares_detectados = determinar_pares_detectados(None)
    print(f"✓ {len(pares_detectados)} pares detectados como similares")
    
    # Calcula total de pares
    total_pares = len(list(combinations(range(len(itens)), 2)))
    
    # Calcula métricas
    print("\nCalculando métricas...")
    metricas = calcular_metricas(pares_esperados, pares_detectados, total_pares)
    metricas_erro = calcular_metricas_erro(pares_esperados, pares_detectados)
    
    # Imprime relatório
    imprimir_relatorio(metricas, metricas_erro, itens)
    
    # Salva relatório em JSON
    print("\nSalvando relatório...")
    salvar_relatorio(metricas, metricas_erro, itens)
    
    return 0


if __name__ == "__main__":
    from itertools import combinations
    exit(main())
