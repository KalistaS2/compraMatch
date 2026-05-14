"""Utilitários para consulta de itens no arquivo JSON do projeto."""

from __future__ import annotations

import json
import unicodedata
import networkx as nx
from pathlib import Path
from typing import Any
import community.community_louvain as community_louvain


ITENS_PATH = Path(__file__).resolve().parents[1] / "json" / "itens.json"
GRAFO_PATH = Path(__file__).resolve().parents[1] / "grafo_Similaridade_70.gexf"

def _normalize_text(valor: str) -> str:
	"""Normaliza texto para comparação: remove acentos e faz casefold.

	Exemplos: "Mobiliário" -> "mobiliario"; "Mobiliario" -> "mobiliario".
	"""
	if valor is None:
		return ""
	s = str(valor)
	nfkd = unicodedata.normalize("NFD", s)
	without_accents = "".join(ch for ch in nfkd if unicodedata.category(ch) != "Mn")
	return without_accents.casefold().strip()


def _normalize_words(valor: str) -> list[str]:
	"""Normaliza uma consulta e separa em palavras úteis para busca."""
	texto_normalizado = _normalize_text(valor)
	return [palavra for palavra in texto_normalizado.split() if palavra]


def encontrar_itens(termo: str, salvar_em: Path | str) -> list[dict[str, Any]]:
	"""Retorna os itens cujo campo de descrição do nó do grafo contenha o termo.

	A busca passa a ser feita diretamente sobre os nós do grafo em
	`GRAFO_PATH`, comparando com o atributo `descricao` de cada nó. A função
	retorna uma lista de dicionários com pelo menos as chaves: `node_id`,
	`descricao_item`, `orgao`, `data`. Se `salvar_em` for fornecido, grava o
	JSON no caminho indicado.
	"""

	palavras_termo = _normalize_words(termo)
	if not palavras_termo:
		return []

	grafo = nx.read_gexf(str(GRAFO_PATH))

	resultados: list[dict[str, Any]] = []
	vistos: set[tuple[str, str]] = set()
	for node_id, attrs in grafo.nodes(data=True):
		descricao = attrs.get("descricao", "")
		descricao_normalizada = _normalize_text(descricao)
		if all(palavra in descricao_normalizada for palavra in palavras_termo):
			orgao = attrs.get("orgao", "")
			chave = (_normalize_text(orgao), _normalize_text(descricao))
			if chave in vistos:
				continue
			vistos.add(chave)
			resultados.append({
				"node_id": str(node_id),
				"descricao_item": descricao,
				"orgao": orgao,
				"data": attrs.get("data", ""),
			})

	if salvar_em is not None:
		destino = Path(salvar_em)
		destino.parent.mkdir(parents=True, exist_ok=True)
		with destino.open("w", encoding="utf-8") as f:
			json.dump(resultados, f, ensure_ascii=False, indent=2, default=str)

	return resultados


def contagem_cluster(termo: str, salvar_em: str | Path | None = None) -> tuple[int, dict[str, Any]]:
	"""Encontra o cluster formado pelos nós que contêm o termo e seus vizinhos (1-hop).

	Esse comportamento limita o cluster ao conjunto de nós que explícita e diretamente
	correspondem ao termo de busca e aos seus vizinhos imediatos, evitando expansão
	transitiva por componentes maiores.

	Retorna uma tupla (quantidade_nos, dados_cluster).
	"""
	palavras_termo = _normalize_words(termo)
	if not palavras_termo:
		return 0, {}

	# Carrega grafo
	grafo = nx.read_gexf(str(GRAFO_PATH))

	# Encontra nós cuja descrição contém o termo
	nos_encontrados = []
	for node_id, atributos in grafo.nodes(data=True):
		descricao = atributos.get("descricao", "")
		descricao_normalizada = _normalize_text(descricao)
		if all(palavra in descricao_normalizada for palavra in palavras_termo):
			nos_encontrados.append(node_id)

	if not nos_encontrados:
		return 0, {}

	# Cluster = nós encontrados + seus vizinhos imediatos (1-hop)
	cluster_nodes = set(nos_encontrados)
	for node_id in list(nos_encontrados):
		for viz in grafo.neighbors(node_id):
			cluster_nodes.add(viz)

	# Constrói dados do cluster com item e suas conexões (apenas para nós em cluster_nodes)
	# Deduplicar: não aceitar mais de um nó com a mesma (orgao, descricao)
	seen_pairs: set[tuple[str, str]] = set()
	included_nodes: set[str] = set()

	for node_id in cluster_nodes:
		atributos = grafo.nodes[node_id]
		descr = atributos.get("descricao", "")
		orgao = atributos.get("orgao", "")
		key = (_normalize_text(orgao), _normalize_text(descr))
		if key in seen_pairs:
			continue
		seen_pairs.add(key)
		included_nodes.add(node_id)

	# Agora constrói dados do cluster apenas com nós incluídos e com conexões filtradas
	dados_cluster = {}
	for node_id in included_nodes:
		atributos = grafo.nodes[node_id]
		vizinhos = [
			{
				"id": vizinho_id,
				"descricao": grafo.nodes[vizinho_id].get("descricao", "")
			}
			for vizinho_id in grafo.neighbors(node_id)
			if vizinho_id in included_nodes
		]
		dados_cluster[node_id] = {
			"item": atributos.get("descricao", ""),
			"orgao": atributos.get("orgao", ""),
			"data": atributos.get("data", ""),
			"conexoes": vizinhos
		}

	# Detecta comunidades dentro do subgrafo restrito aos nós incluídos
	try:
		subgrafo = grafo.subgraph(included_nodes).copy()
		# community_louvain espera grafos não direcionados em geral
		if hasattr(subgrafo, "to_undirected"):
			subgrafo_und = subgrafo.to_undirected()
		else:
			subgrafo_und = subgrafo

		particao = community_louvain.best_partition(subgrafo_und)

		# Agrupa nós por comunidade
		comunidades: dict[str, list[dict[str, str]]] = {}
		for nodo, comm in particao.items():
			com_id = str(comm)
			comunidades.setdefault(com_id, []).append({
				"id": nodo,
				"descricao": grafo.nodes[nodo].get("descricao", ""),
				"orgao": grafo.nodes[nodo].get("orgao", "")
			})

		# Anexa informações de comunidades aos dados do cluster
		dados_cluster["comunidades"] = comunidades

		# Exibe comunidades no stdout
		print("Comunidades detectadas:")
		for com_id, membros in comunidades.items():
			print(f"  Comunidade {com_id}: {len(membros)} membros")
			for m in membros:
				print(f"    - {m['id']}: {m['descricao']} ({m['orgao']})")

	except Exception as e:
		# Se houver falha na detecção de comunidades, registre no JSON e prossiga
		dados_cluster["comunidades_error"] = str(e)

	# Salva em JSON se especificado (ou padrão)
	if salvar_em is None:
		salvar_em = ITENS_PATH.parent / f"cluster_{_normalize_text(termo).replace(' ', '_')}.json"
    
	destino = Path(salvar_em)
	destino.parent.mkdir(parents=True, exist_ok=True)
	with destino.open("w", encoding="utf-8") as f:
		json.dump(dados_cluster, f, ensure_ascii=False, indent=2, default=str)

	return len(included_nodes), dados_cluster


def listar_descricoes_cluster(dados_cluster: dict[str, Any], termo: str, salvar_em: str | Path | None = None) -> list[str]:
	"""Extrai apenas as descrições únicas dos nós do cluster e retorna lista.

	Args:
	    dados_cluster: dicionário retornado por contagem_cluster
	    termo: termo usado na busca (para nomeação do arquivo)
	    salvar_em: caminho para salvar o JSON. Se None, salva em ``json/descricoes_{termo}.json``

	Returns:
	    Lista de descrições únicas dos nós
	"""
	# Usa dict.fromkeys para manter ordem e remover duplicatas
	descricoes_unicas = list(dict.fromkeys(
		item_data.get("item", "")
		for item_data in dados_cluster.values()
		if item_data.get("item", "")
	))

	# Salva em JSON se houver dados
	if descricoes_unicas:
		if salvar_em is None:
			salvar_em = ITENS_PATH.parent / f"descricoes_{_normalize_text(termo).replace(' ', '_')}.json"
		
		destino = Path(salvar_em)
		destino.parent.mkdir(parents=True, exist_ok=True)
		with destino.open("w", encoding="utf-8") as f:
			json.dump(descricoes_unicas, f, ensure_ascii=False, indent=2)

	return descricoes_unicas


if __name__ == "__main__":
	consulta = input("Digite o termo de busca: ")
	
	# Busca itens
	local = Path(__file__).resolve().parents[1] / "json" / f"resultados_busca_{consulta}.json"
	resultados = encontrar_itens(consulta, local)
	print(f"Encontrados {len(resultados)} itens.")
	print(f"Arquivo salvo em: {local}")
	
	# Busca cluster
	num_nos, dados = contagem_cluster(consulta)
	print(f"Cluster encontrado com {num_nos} nós.")
	if num_nos > 0:
		nome_arquivo = f"cluster_{_normalize_text(consulta).replace(' ', '_')}.json"
		print(f"Arquivo salvo em: {ITENS_PATH.parent / nome_arquivo}")
		
		# Extrai e salva apenas as descrições
		descricoes = listar_descricoes_cluster(dados, consulta)
		nome_descricoes = f"descricoes_{_normalize_text(consulta).replace(' ', '_')}.json"
		print(f"Descrições salvas em: {ITENS_PATH.parent / nome_descricoes} ({len(descricoes)} itens)")