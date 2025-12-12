import os
import json
import pickle
from flask import Flask, render_template, jsonify
from orgaos import extrair_orgaos

app = Flask(__name__, template_folder='../templates', static_folder='../static')

# Caminhos dos arquivos (relativos ao diretório api)
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ITENS_FILE = os.path.join(PROJECT_ROOT, 'itens.json')
GRAFO_FILE = os.path.join(PROJECT_ROOT, 'grafo_Similaridade_90_porcento.gpickle')

def load_items_from_json(path=ITENS_FILE):
    """Carrega itens do arquivo JSON."""
    items = []
    if not path or not os.path.exists(path):
        return items
    
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = f.read()
    except Exception:
        return items
    
    decoder = json.JSONDecoder()
    idx = 0
    length = len(data)
    while True:
        while idx < length and data[idx].isspace():
            idx += 1
        if idx >= length:
            break
        try:
            obj, end = decoder.raw_decode(data, idx)
        except json.JSONDecodeError:
            break
        idx = end
        if isinstance(obj, list):
            items.extend(obj)
        else:
            items.append(obj)
    
    return items

def load_graph():
    """Carrega o grafo do arquivo gpickle."""
    if not os.path.exists(GRAFO_FILE):
        return None
    
    try:
        with open(GRAFO_FILE, 'rb') as f:
            graph = pickle.load(f)
        return graph
    except Exception:
        return None

@app.route('/')
def home():
    """Página inicial com estatísticas."""
    try:
        lista_orgaos = extrair_orgaos(ITENS_FILE)
        total_usuarios = len(lista_orgaos)
        
        # Carrega grafo e conta nós
        grafo = load_graph()
        total_itens = 0
        if grafo is not None:
            if hasattr(grafo, 'nodes'):  # NetworkX graph
                total_itens = len(grafo.nodes())
            elif isinstance(grafo, dict) and 'nodes' in grafo:  # Dict representation
                total_itens = len(grafo['nodes'])
        
        # Carrega total de itens do JSON
        items_json = load_items_from_json()
        total_itens_json = len(items_json)
        
        # Conta itens distintos (compras ativas)
        # Dois itens são iguais se tiverem mesma descrição e mesmo órgão
        unique_map = {}
        for item in items_json:
            key = f"{item.get('descricao_item')}|{item.get('nomeUnidade')}"
            if key not in unique_map:
                unique_map[key] = item
        
        total_compras_ativas = len(unique_map)
        
        return render_template('home.html', 
                             total_usuarios=total_usuarios, 
                             total_itens_grafo=total_itens,
                             total_itens_json=total_itens_json,
                             total_compras_ativas=total_compras_ativas)
    except Exception as e:
        print(f"Erro ao carregar home: {e}")
        return render_template('home.html', total_usuarios=0, total_itens_grafo=0, total_itens_json=0, total_compras_ativas=0)

@app.route('/api/orgaos')
def api_orgaos():
    """API para obter lista de órgãos."""
    try:
        lista_orgaos = extrair_orgaos(ITENS_FILE)
        return jsonify({'orgaos': lista_orgaos, 'total': len(lista_orgaos)})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/itens')
def api_itens():
    """API para obter lista de itens."""
    try:
        items = load_items_from_json()
        return jsonify({'itens': items, 'total': len(items)})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/top-items')
def api_top_items():
    """API para obter top itens para as compras ativas."""
    try:
        items = load_items_from_json()
        # Retorna os primeiros 5 itens com descrição
        top_items = [item for item in items if item.get('descricao_item')][:5]
        return jsonify({'items': top_items})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/grafo')
def api_grafo():
    """API para obter dados do grafo em formato JSON."""
    try:
        grafo = load_graph()
        
        if grafo is None:
            return jsonify({'nodes': [], 'edges': []})
        
        # Se for NetworkX graph
        if hasattr(grafo, 'nodes'):
            nodes = []
            edges = []
            
            # Extrai nós com atributos
            for node_id in grafo.nodes():
                node_data = grafo.nodes[node_id]
                nodes.append({
                    'id': str(node_id),
                    'label': node_data.get('descricao', '')[:50] + '...',
                    'orgao': node_data.get('orgao', ''),
                    'descricao': node_data.get('descricao', ''),
                    'title': node_data.get('descricao', '')
                })
            
            # Extrai arestas
            for u, v, data in grafo.edges(data=True):
                edges.append({
                    'source': str(u),
                    'target': str(v),
                    'weight': data.get('weight', 0.5)
                })
            
            return jsonify({'nodes': nodes, 'edges': edges, 'total_nodes': len(nodes), 'total_edges': len(edges)})
        
        # Se for dict representation
        elif isinstance(grafo, dict) and 'nodes' in grafo:
            return jsonify(grafo)
        
        return jsonify({'nodes': [], 'edges': []})
    except Exception as e:
        print(f"Erro ao carregar grafo: {e}")
        return jsonify({'error': str(e), 'nodes': [], 'edges': []}), 500

@app.route('/grafo')
def grafo():
    """Página de visualização do grafo."""
    return render_template('grafo.html')

@app.route('/itens')
def itens():
    """Página de listagem de itens."""
    return render_template('itens.html')

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
