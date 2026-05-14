"""Analisa um arquivo de cluster e calcula métricas de avaliação.

Uso: execute o módulo apontando para o JSON do cluster e o JSON com as descrições
do conjunto de avaliação. Exemplo:

python -m baseline.analisador_caso_real \ 
    --cluster json/cluster_teste.json \ 
    --dataset json/descricoes_agua_mineral.json

O script contará verdadeiros positivos/negativos, falsos positivos/negativos
com base nas listas `SIMILARES` e `NAO_SIMILARES` definidas abaixo e imprimirá
precision, recall, f1 e accuracy.
"""
from __future__ import annotations

import argparse
import json
import unicodedata
from pathlib import Path
from typing import Iterable


SIMILARES = {
    "ÁGUA MINERAL, Composição: água mineral natural, SEM GÁS; Produto em conformidade com a legislação em vigor; Unidade de Fornecimento: garrafa pet de 500mL.",
    "Água mineral natural, sem gás, em copos plásticos descartáveis de 200ml - Caixa com 48 unidades",
    "ÁGUA MINERAL BOMBONA DE 20 LITROS.",
    "AGUA MINERAL COPO DE 200 ML CX  COM 48 UNIDADES",
    "ÁGUA MINERAL EM COPO 200 ML",
    "ÁGUA MINERAL, Composição: água mineral natural, SEM GÁS; Produto em conformidade com a legislação em vigor; Unidade de Fornecimento: garrafa pet de 350mL.",
    "ÁGUA MINERAL, Composição: água mineral natural, SEM GÁS; Produto em conformidade com a legislação em vigor; Fornecimento de embalagem retornável em regime de comodato; Unidade de Fornecimento: garrafão retornável de 20L.",
    "ÁGUA MINERAL, Composição: água mineral natural, SEM GÁS; Produto em conformidade com a legislação em vigor; Unidade de Fornecimento: garrafão retornável de 20L.",
    "AGUA MINERAL GARRAFÃO DE 20 LITROS",
    "ÁGUA MINERAL, EMBALAGEM DE 5 LITROS.",
    "ÁGUA 20 L",
    "ÁGUA MINERAL SEM GÁS",
    "ÁGUA MINERAL, EMBALAGEM DE 500 ML.",
}

NAO_SIMILARES = {
    "GALÃO DE 20 LITROS VAZIO PARA ÁGUA MINERAL. VALIDADE 3 ANOS",
    "ÁGUA DESTILADA, COM 5 LITROS",
    "BOTA DE UNNA, BANDAGEM PRONTA PARA USO, COMPOSTA POR  30% ALGODÃO 70 % POLIESTER NÃO ESTÉRIL, INELÁSTICA, EMBALADA INDIVIDUALMENTE, IMPREGNADA COM PASTA CONTENDO NO MÌNIMO: 23 %  ÓXIDO DE ZINCO, COMPROVADO ATRÁVES DE LAUDO TÉCNICO,ÁGUA DESTILADA, GLICEROL, ÓLEO MINERAL, ESTABILIZANTE/ESPESSANTE, CONSERVANTE (ANTIFUNGICO E ANTIBACTERIANO), COM ACABAMENTO NAS BORDAS E ISENTO DE ODORES. EMBALADA INDIVIDUALMENTE ENROLADA SOBRE UMA BASE DE PLÁSTICO, ACONDICIONADA NUM INVÓLUCRO E SELADA DENTRO DE UM SACO DE POLIETILENO EMBALADO NUMA CAIXA DE CARTÃO. NÃO ESTÉRIL. TAMANHO 10,16 CM X 9,14 MT. ,APRESENTAR LAUDO JUNTO A PROPOSTA DE PREÇOS, A BULA DO PRODUTO E DECLARAÇÃO DA EMPRESA VENCEDORA INDICANDO OS DADOS DA ENFERMEIRA A QUAL FARÁ O TREINAMENTO E ACOMPANHAMENTO DO USO DO PRODUTO SOLICITADO, DEVERÁ AINDA APRESENTAR CERTIFICADO DE FORMAÇÃO DO CURSO DE PÓS-GRADUAÇÃO EM   ESTOMOTERAPIA.",
    "LIMPADOR DESENGORDURANTE 500 ML",
    "BICARBONATO DE SÓDIO - EMBALAGEM  DE 500G",
    "SABÃO LÍQUIDO 5LTS",
    "ÁGUA SANITÁRIA EMB DE 5 LTS  ",
    "SUCO NATURAL DE 500ML SABOR DA FRUTA A ESCOLHER (SE NECESSÁRIO DISPONIBILIZAR EMBALAGEM)",
    "ÁGUA MINERAL, Material: água mineral natural, Gaseificação: sem gás, Unidade de Fornecimento: garrafa pet de 350 ml, Características Adicionais: com rótulo personalizado conforme Termo de Referência.",
    "AGUA DESMINERALIZADA PARA RADIADOR",
}


def normalize(text: str) -> str:
    if text is None:
        return ""
    s = str(text)
    nfkd = unicodedata.normalize("NFD", s)
    without_accents = "".join(ch for ch in nfkd if unicodedata.category(ch) != "Mn")
    return " ".join(without_accents.casefold().split())


def load_cluster(cluster_path: Path) -> list[str]:
    data = json.loads(cluster_path.read_text(encoding="utf-8"))
    # dados_cluster has keys for node ids and possibly 'comunidades' or errors
    descriptions = []
    for k, v in data.items():
        if k in ("comunidades", "comunidades_error"):
            continue
        if isinstance(v, dict):
            descr = v.get("item") or v.get("descricao") or ""
            if descr:
                descriptions.append(descr)
        elif isinstance(v, str):
            descriptions.append(v)
    return descriptions


def load_dataset(dataset_path: Path) -> list[str]:
    return json.loads(dataset_path.read_text(encoding="utf-8"))


def evaluate(cluster_descs: Iterable[str], dataset: Iterable[str]):
    cluster_set = {normalize(d) for d in cluster_descs}

    similares_norm = {normalize(s) for s in SIMILARES}
    nao_sim_norm = {normalize(s) for s in NAO_SIMILARES}

    tp = fp = tn = fn = 0
    labeled = 0
    ignored = 0

    for d in dataset:
        nd = normalize(d)
        if nd in similares_norm:
            label = 1
        elif nd in nao_sim_norm:
            label = 0
        else:
            ignored += 1
            continue

        labeled += 1
        predicted = 1 if nd in cluster_set else 0

        if predicted == 1 and label == 1:
            tp += 1
        elif predicted == 1 and label == 0:
            fp += 1
        elif predicted == 0 and label == 1:
            fn += 1
        elif predicted == 0 and label == 0:
            tn += 1

    precision = tp / (tp + fp) if (tp + fp) > 0 else None
    recall = tp / (tp + fn) if (tp + fn) > 0 else None
    f1 = None
    if precision is not None and recall is not None and (precision + recall) > 0:
        f1 = 2 * precision * recall / (precision + recall)
    accuracy = (tp + tn) / labeled if labeled > 0 else None

    return {
        "tp": tp,
        "fp": fp,
        "tn": tn,
        "fn": fn,
        "errados": fp + fn,
        "precision": precision,
        "recall": recall,
        "f1": f1,
        "accuracy": accuracy,
        "labeled": labeled,
        "ignored": ignored,
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--cluster", required=True, help="Caminho para o JSON de cluster")
    p.add_argument("--dataset", required=True, help="Caminho para o JSON com descrições (lista)")
    p.add_argument("--save", required=False, help="Arquivo de saída para métricas (JSON)")
    args = p.parse_args()

    cluster_path = Path(args.cluster)
    dataset_path = Path(args.dataset)

    cluster_descs = load_cluster(cluster_path)
    dataset = load_dataset(dataset_path)

    results = evaluate(cluster_descs, dataset)

    print("Resultados da avaliação:")
    for k, v in results.items():
        print(f"  {k}: {v}")

    if args.save:
        Path(args.save).write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
