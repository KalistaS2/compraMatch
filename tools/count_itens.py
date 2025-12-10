import json
p = 'itens.json'
try:
    with open(p, 'r', encoding='utf-8') as f:
        s = f.read()
except Exception as e:
    print('Erro lendo', p, e)
    raise SystemExit(1)

decoder = json.JSONDecoder()
idx = 0
length = len(s)
items = []
while True:
    while idx < length and s[idx].isspace():
        idx += 1
    if idx >= length:
        break
    try:
        obj, end = decoder.raw_decode(s, idx)
    except Exception:
        # termina se não for possível decodificar mais
        break
    idx = end
    if isinstance(obj, list):
        items.extend(obj)
    else:
        items.append(obj)

print('itens.json ->', len(items), 'itens lidos')
