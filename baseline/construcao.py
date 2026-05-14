import json
import os
import pickle
import unicodedata
import networkx as nx
import similaridadeBase
# Caminho para o arquivo JSON
json_path = os.path.join(os.path.dirname(__file__), '../json/itensSinteticos.json')

def carregar_itens():
    """Carrega todos os itens do arquivo JSON"""
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            dados = json.load(f)
        
        licitacoes = dados.get('licitacoes_publicas', {})
        itens = []
        
        # Extrai itens de cada categoria
        for categoria, items_dict in licitacoes.items():
            for nome_item, caracteristicas in items_dict.items():
                item = {
                    'nome_item': nome_item,
                    'classe_item': categoria,
                    'caracteristica1': {'nome': 'caracteristica1', 'opcoes': []},
                    'caracteristica2': {'nome': 'caracteristica2', 'opcoes': []},
                    'caracteristica3': {'nome': 'caracteristica3', 'opcoes': []}
                }
                
                # Mapeia as características
                cara_keys = list(caracteristicas.keys())
                for idx, key in enumerate(cara_keys[:3]):  # Pega até 3 características
                    cara_num = f'caracteristica{idx + 1}'
                    item[cara_num] = {
                        'nome': key,
                        'opcoes': caracteristicas[key] if isinstance(caracteristicas[key], list) else []
                    }
                
                itens.append(item)
        
        return itens
    except FileNotFoundError:
        print(f"Erro: Arquivo {json_path} não encontrado")
        return []
    except json.JSONDecodeError:
        print("Erro: Arquivo JSON inválido")
        return []

def carregar_itens_complexos():
    """Carrega itens do arquivo itens_complexos.json"""
    complexos_path = os.path.join(os.path.dirname(__file__), '../json/itens_complexos.json')
    try:
        with open(complexos_path, 'r', encoding='utf-8') as f:
            dados = json.load(f)
        return dados.get('itens', [])
    except FileNotFoundError:
        print(f"Erro: Arquivo {complexos_path} não encontrado")
        return []
    except json.JSONDecodeError:
        print("Erro: Arquivo JSON inválido")
        return []

def processar_itens():
    """Processa itens complexos e cria array de similaridades"""
    itens = carregar_itens_complexos()
    
    if not itens:
        print("Nenhum item encontrado no arquivo itens_complexos.json")
        return
    
    print(f"Total de itens carregados: {len(itens)}\n")
    
    # Extrai primeira palavra do nome de cada item
    nomes = [item.get('nome_item', '').split()[0] if item.get('nome_item') else '' for item in itens]
    
    # Cria array de similaridades
    resultado_itens = []
    
    for i, item in enumerate(itens):
        nome_item = item.get('nome_item', 'N/A')
        classe_item = item.get('classe_item', 'N/A')
        primeira_palavra_i = nomes[i]
        
        # Array de comparações deste item com todos os outros
        similaridades = []
        
        for j, outro_item in enumerate(itens):
            nome_outro = outro_item.get('nome_item', 'N/A')
            primeira_palavra_j = nomes[j]
            
            # Comparação: similar se primeira palavra for igual
            similar = 1 if primeira_palavra_i == primeira_palavra_j else 0
            
            similaridades.append({
                'indice': j,
                'item': nome_outro,
                'similar': similar
            })
        
        # Adiciona item com suas similaridades
        resultado_itens.append({
            'indice': i,
            'item': nome_item,
            'classe': classe_item,
            'primeira_palavra': primeira_palavra_i,
            'similaridade': similaridades
        })
        
        # Exibe progressão
        if (i + 1) % max(1, len(itens) // 10) == 0:
            print(f"Processados {i + 1}/{len(itens)} itens...")
    
    # Salva resultado
    output_path = os.path.join(os.path.dirname(__file__), '../json/array_similaridade_complexos.json')
    
    resultado = {
        'total_itens': len(itens),
        'itens': resultado_itens
    }
    
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(resultado, f, ensure_ascii=False, indent=2)
        print(f"\nArray de similaridades salvo em: {output_path}")
        print(f"Total de itens processados: {len(itens)}")
    except IOError as e:
        print(f"Erro ao salvar arquivo: {e}")

def criar_itens():
    """Cria todas as combinações possíveis de itens com suas características"""
    itens = carregar_itens()
    
    if not itens:
        print("Nenhum item encontrado no JSON")
        return
    
    itens_complexos = []
    count = 0
    for item in itens:
        nome_item = item.get('nome_item', 'N/A')
        print(f"criando itens complexos do item: {nome_item}")
        count += 1
        classe_item = item.get('classe_item', 'N/A')
        
        # Extrai as opções de cada característica
        opcoes_cara1 = item.get('caracteristica1', {}).get('opcoes', [])
        opcoes_cara2 = item.get('caracteristica2', {}).get('opcoes', [])
        opcoes_cara3 = item.get('caracteristica3', {}).get('opcoes', [])
        
        nome_cara1 = item.get('caracteristica1', {}).get('nome', 'caracteristica1')
        nome_cara2 = item.get('caracteristica2', {}).get('nome', 'caracteristica2')
        nome_cara3 = item.get('caracteristica3', {}).get('nome', 'caracteristica3')
        
        # Itera sobre todas as combinações possíveis
        for i, opcao1 in enumerate(opcoes_cara1):
            for j, opcao2 in enumerate(opcoes_cara2):
                for k, opcao3 in enumerate(opcoes_cara3):
                    # Concatena nome do item com todas as opções
                    nome_completo = f"{nome_item} {opcao1} {opcao2} {opcao3}"
                    
                    item_complexo = {
                        'classe_item': classe_item,
                        'nome_item': nome_completo
                    }
                    itens_complexos.append(item_complexo)
    # Salva em arquivo JSON
    output_path = os.path.join(os.path.dirname(__file__), '../json/itens_complexos.json')
    
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump({'itens': itens_complexos}, f, ensure_ascii=False, indent=2)
        print(f"Sucesso! {len(itens_complexos)} itens complexos salvos em: {output_path}, \ntotal de combinações criadas: {count}")
    except IOError as e:
        print(f"Erro ao salvar arquivo: {e}")

def comparar_arrays(threshold=0.7):
    """
    Compara o array baseline com o array Gemma e calcula:
    - VP: Verdadeiros Positivos
    - FP: Falsos Positivos
    - VN: Verdadeiros Negativos
    - FN: Falsos Negativos
    """
    # Carrega os dois arrays
    baseline_path = os.path.join(os.path.dirname(__file__), '../json/array_similaridade_complexos.json')
    gemma_path = os.path.join(os.path.dirname(__file__), '../json/array_similaridade_gemma.json')
    
    try:
        with open(baseline_path, 'r', encoding='utf-8') as f:
            baseline = json.load(f)
        with open(gemma_path, 'r', encoding='utf-8') as f:
            gemma = json.load(f)
    except FileNotFoundError as e:
        print(f"Erro ao carregar arquivos: {e}")
        return
    except json.JSONDecodeError as e:
        print(f"Erro ao decodificar JSON: {e}")
        return
    
    if not baseline.get('itens') or not gemma.get('itens'):
        print("Nenhum item encontrado nos arrays")
        return
    
    print(f"Comparando {len(baseline['itens'])} itens do baseline com Gemma...\n")
    
    vp = 0  # Verdadeiros Positivos
    fp = 0  # Falsos Positivos
    vn = 0  # Verdadeiros Negativos
    fn = 0  # Falsos Negativos
    
    erros_absolutos = []  # Para calcular MAE
    erros_quadraticos = []  # Para calcular RMSE
    
    # Itera sobre cada item do baseline
    for i, item_baseline in enumerate(baseline['itens']):
        if i >= len(gemma['itens']):
            break
        
        item_gemma = gemma['itens'][i]
        baseline_sims = item_baseline['similaridade']
        gemma_sims = item_gemma['similaridade']
        
        # Compara cada similaridade
        for j in range(len(baseline_sims)):
            if j >= len(gemma_sims):
                break
            
            # Baseline usa 0 ou 1
            baseline_similar = baseline_sims[j]['similar']
            
            # Gemma usa score float, converte com threshold
            gemma_score = gemma_sims[j]['similaridade']
            gemma_similar = 1 if gemma_score >= threshold else 0
            
            # Calcula erro absoluto e quadrático para MAE e RMSE
            erro_absoluto = abs(baseline_similar - gemma_score)
            erros_absolutos.append(erro_absoluto)
            erros_quadraticos.append(erro_absoluto ** 2)
            
            # Calcula VP, FP, VN, FN
            if baseline_similar == 1 and gemma_similar == 1:
                vp += 1  # Ambos dizem que é similar - VP
            elif baseline_similar == 0 and gemma_similar == 1:
                fp += 1  # Baseline diz não similar, Gemma diz similar - FP
            elif baseline_similar == 0 and gemma_similar == 0:
                vn += 1  # Ambos dizem que não é similar - VN
            elif baseline_similar == 1 and gemma_similar == 0:
                print("falso similar: ", baseline_sims[i]['item'], " + ", gemma_sims[j]['item'], "similaridade gemma: ", gemma_sims[j]['similaridade'])
                fn += 1  # Baseline diz similar, Gemma diz não similar - FN
                print("-"*60)
    
    # Calcula métricas
    total = vp + fp + vn + fn
    acuracia = (vp + vn) / (vp + fp + vn + fn) if total > 0 else 0
    precisao = vp / (vp + fp) if (vp + fp) > 0 else 0
    recall = vp / (vp + fn) if (vp + fn) > 0 else 0
    f1 = 2 * (precisao * recall) / (precisao + recall) if (precisao + recall) > 0 else 0
    
    # Calcula MAE e RMSE
    mae = sum(erros_absolutos) / len(erros_absolutos) if erros_absolutos else 0
    rmse = (sum(erros_quadraticos) / len(erros_quadraticos)) ** 0.5 if erros_quadraticos else 0
    
    # Exibe resultados
    print("="*60)
    print("RESULTADOS DA COMPARAÇÃO")
    print("="*60)
    print(f"\nMatriz de Confusão:")
    print(f"  Verdadeiros Positivos (VP):  {vp}")
    print(f"  Falsos Positivos (FP):       {fp}")
    print(f"  Verdadeiros Negativos (VN):  {vn}")
    print(f"  Falsos Negativos (FN):       {fn}")
    print(f"\nTotal de comparações: {total}")
    
    print(f"\nMétricas:")
    print(f"  Acurácia:  {acuracia:.4f} ({acuracia*100:.2f}%)")
    print(f"  Precisão:  {precisao:.4f} ({precisao*100:.2f}%)")
    print(f"  Recall: {recall:.4f} ({recall*100:.2f}%)")
    print(f"  F1-Score:  {f1:.4f}")    
    print(f"\nErros:")
    print(f"  MAE (Erro Médio Absoluto):  {mae:.4f}")
    print(f"  RMSE (Raiz do Erro Quadrático Médio): {rmse:.4f}")    
    print(f"\nTaxa de Acertos Positivos (TP Rate / Sensitivity): {vp/(vp+fn) if (vp+fn) > 0 else 0:.4f}")
    print(f"Taxa de Acertos Negativos (TN Rate / Specificity): {vn/(vn+fp) if (vn+fp) > 0 else 0:.4f}")
    
    print("="*60)
    
    # Create results dictionary with threshold
    resultado = {
        'threshold': round(threshold *100, 2),
        'vp': vp,
        'fp': fp,
        'vn': vn,
        'fn': fn,
        'acuracia': round(acuracia * 100, 2),
        'precisao': round(precisao * 100, 2),
        'recall': round(recall * 100, 2),
        'f1': round(f1 * 100, 2),
        'mae': round(mae * 100, 2),
        'rmse': rmse
    }

    # Load existing results or create new list
    resultados_path = os.path.join(os.path.dirname(__file__), '../json/resultados.json')
    resultados = []

    try:
        with open(resultados_path, 'r', encoding='utf-8') as f:
            resultados = json.load(f)
    except FileNotFoundError:
        resultados = []

    # Append new result
    resultados.append(resultado)

    # Save to file
    try:
        with open(resultados_path, 'w', encoding='utf-8') as f:
            json.dump(resultados, f, ensure_ascii=False, indent=2)
        print(f"Resultados salvos em: {resultados_path}")
    except IOError as e:
        print(f"Erro ao salvar resultados: {e}")
    
    

if __name__ == '__main__':
    print("="*60)
    print("ETAPA 1: Criando itens complexos...")
    print("="*60)
    criar_itens()
    
    print("\n" + "="*60)
    print("ETAPA 2: Processando itens e gerando baseline de similaridade...")
    print("="*60 + "\n")
    processar_itens()
    
    print("\n" + "="*60)
    print("ETAPA 3: Calculando similaridades com Gemma Embeddings...")
    print("="*60 + "\n")
    similaridadeBase.similaridades_baseline(salvar_json=True)

    threshold = 0.7
    # while threshold <= 1:
    # threshold += 0.05
    print("\n" + "="*60)
    print(f"ETAPA 4: Comparando resultados baseline vs Gemma com threshold {threshold}...")
    print("="*60 + "\n")
    comparar_arrays(threshold)

