import json
import os
from typing import List


def _iter_json_blocks(path: str):
    """Itera objetos JSON em um arquivo que pode conter múltiplos blocos JSON
    (por exemplo, vários arrays escritos em append). Retorna cada valor decodificado.
    """
    if not path or not os.path.exists(path):
        return
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = f.read()
    except Exception:
        return

    decoder = json.JSONDecoder()
    idx = 0
    length = len(data)
    while True:
        # skip whitespace
        while idx < length and data[idx].isspace():
            idx += 1
        if idx >= length:
            break
        try:
            obj, end = decoder.raw_decode(data, idx)
        except json.JSONDecodeError:
            break
        idx = end
        yield obj


def extrair_orgaos(path: str = "itens.json") -> List[str]:
    """
    Lê `path` e retorna uma lista de nomes de órgãos distintos encontrados no campo
    `nomeUnidade`. A ordem é a de primeira ocorrência no arquivo.

    Se o arquivo não existir ou estiver vazio, retorna lista vazia.
    """
    seen = set()
    result = []
    for block in _iter_json_blocks(path):
        # cada bloco pode ser uma lista de itens ou um único objeto
        items = block if isinstance(block, list) else [block]
        for item in items:
            if not isinstance(item, dict):
                continue
            nome = item.get('nomeUnidade')
            if nome and nome not in seen:
                seen.add(nome)
                result.append(nome)
    return result


if __name__ == "__main__":
    # execução rápida para debug
    orgaos = extrair_orgaos()
    print(f"{len(orgaos)} orgaos distintos encontrados")
    for o in orgaos[:50]:
        print(o)
