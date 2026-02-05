"""
Módulo de construção de dataset sintético para baseline de canetas.
Cria um produto cartesiano de tipos, cores, formatos e fabricantes.
"""

import json
import itertools
from pathlib import Path


def criar_listas_base():
    """
    Cria as listas base de características de canetas.
    
    Retorna:
        dict: Dicionário com as listas: tipos, cores, formatos, empresas
    """
    tipos = [
        "caneta esferográfica",
        "caneta gel",
        "caneta tinteiro",
        "caneta rollerball",
        "caneta canetão",
        "caneta esferográfica premium",
        "caneta gel premium",
        "caneta tinteiro premium",
        "caneta rollerball premium",
        "caneta canetão premium"
    ]
    
    cores = [
        "preta",
        "azul",
        "vermelha",
        "verde",
        "roxo",
        "rosa",
        "laranja",
        "marrom",
        "cinza",
        "branca"
    ]
    
    formatos = [
        "fina",
        "média",
        "grossa",
        "extra grossa",
        "retrátil",
        "com tampa",
        "de ponta arredondada",
        "de ponta afiada",
        "com clip",
        "sem clip"
    ]
    
    empresas = [
        "BIC",
        "Pilot",
        "Faber-Castell",
        "Stabilo",
        "Pentel",
        "Mitsubishi",
        "Caran d'Ache",
        "Staedtler",
        "Lamy",
        "Montblanc"
    ]
    
    return {
        "tipos": tipos,
        "cores": cores,
        "formatos": formatos,
        "empresas": empresas
    }


def gerar_itens_sinteticos(listas_base):
    """
    Gera itens sintéticos usando produto cartesiano das listas base.
    
    Args:
        listas_base: dict com as listas base
        
    Retorna:
        list: Lista de itens sintéticos com estrutura compatível com similaridades.py
    """
    tipos = listas_base["tipos"]
    cores = listas_base["cores"]
    formatos = listas_base["formatos"]
    empresas = listas_base["empresas"]
    
    itens = []
    idx = 0
    
    # Produto cartesiano: tipo × cor × formato × empresa
    for tipo, cor, formato, empresa in itertools.product(tipos, cores, formatos, empresas):
        descricao = f"{tipo} {cor} {formato} {empresa}".lower()
        
        item = {
            "descricao_item": descricao,
            "nomeUnidade": empresa,  # Usa a empresa como unidade para garantir órgãos distintos
            "data_desejada": "2026-02-05",
            "tipo": tipo,
            "cor": cor,
            "formato": formato,
            "empresa": empresa,
            "idx": idx
        }
        
        itens.append(item)
        idx += 1
    
    return itens


def salvar_itens_json(itens, caminho="itensSinteticos.json"):
    """
    Salva os itens sintéticos em arquivo JSON.
    
    Args:
        itens: lista de itens a salvar
        caminho: caminho do arquivo de saída
    """
    # Converte caminho relativo para absoluto no diretório baseline/
    arquivo_path = Path(__file__).parent / caminho
    
    with open(arquivo_path, 'w', encoding='utf-8') as f:
        json.dump(itens, f, ensure_ascii=False, indent=2)
    
    print(f"✓ {len(itens)} itens sintéticos salvos em: {arquivo_path}")
    return str(arquivo_path)


def main():
    """Função principal para construir o dataset sintético."""
    print("=" * 60)
    print("CONSTRUÇÃO DE BASELINE SINTÉTICA")
    print("=" * 60)
    
    # Cria as listas base
    listas_base = criar_listas_base()
    
    print(f"\n✓ Tipos de canetas: {len(listas_base['tipos'])}")
    print(f"✓ Cores: {len(listas_base['cores'])}")
    print(f"✓ Formatos: {len(listas_base['formatos'])}")
    print(f"✓ Empresas: {len(listas_base['empresas'])}")
    
    # Calcula produto cartesiano
    total_esperado = (
        len(listas_base['tipos']) * 
        len(listas_base['cores']) * 
        len(listas_base['formatos']) * 
        len(listas_base['empresas'])
    )
    print(f"\n✓ Total de itens esperados (produto cartesiano): {total_esperado}")
    
    # Gera itens sintéticos
    print("\nGerando itens sintéticos...")
    itens = gerar_itens_sinteticos(listas_base)
    print(f"✓ Itens gerados: {len(itens)}")
    
    # Salva em JSON
    print("\nSalvando em JSON...")
    caminho = salvar_itens_json(itens)
    
    print("\n" + "=" * 60)
    print(f"BASELINE SINTÉTICA CRIADA COM SUCESSO!")
    print("=" * 60)
    
    return itens, listas_base, caminho


if __name__ == "__main__":
    main()
