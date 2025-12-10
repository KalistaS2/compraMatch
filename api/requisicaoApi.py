from datetime import date, datetime
import json

import requests
from model.items import PcaItem


def request(anoPca="2024", max_items=1000, tamanhoPagina="90", url="", salvar_arquivo=True, minPagina=1, maxPagina=5):
    # Create an empty list to store items
    items_list = []
    buffer = []
    print("Iniciando requisição à API do PNCP...")

    for pagina in range(minPagina, maxPagina):
        for cod in range(1, 50):
            # Parâmetros aceitos pela API
            params = {
                "anoPca": anoPca,
                "codigoClassificacaoSuperior": cod,
                "pagina": pagina,
                "tamanhoPagina": tamanhoPagina
            }
            headers = {"accept": "*/*"}

            response = requests.get(url, headers=headers, params=params)

            if response.status_code == 200:
                data = response.json()


                for pca in data.get("data", []):
                    for item in pca.get("itens", []):
                        # Conversões seguras de data/hora
                        data_inclusao = datetime.fromisoformat(item["dataInclusao"]) if item.get("dataInclusao") else None
                        data_atualizacao = datetime.fromisoformat(item["dataAtualizacao"]) if item.get("dataAtualizacao") else None
                        data_desejada = date.fromisoformat(item["dataDesejada"]) if item.get("dataDesejada") else None

                        # Criação do objeto PcaItem com todos os parâmetros se for Material
                        if (item.get("nomeClassificacaoCatalogo") == "Material"):
                            pca_item = PcaItem(
                                descricao_item=item.get("descricaoItem"),
                                nome_classificacao_catalogo=item.get("nomeClassificacaoCatalogo"),
                                quantidade_estimada=item.get("quantidadeEstimada", 0),
                                pdm_codigo=item.get("pdmCodigo"),
                                data_inclusao=data_inclusao,
                                numero_item=item.get("numeroItem", 0),
                                data_atualizacao=data_atualizacao,
                                valor_total=item.get("valorTotal", 0),
                                pdm_descricao=item.get("pdmDescricao"),
                                codigo_item=item.get("codigoItem"),
                                unidade_requisitante=item.get("unidadeRequisitante"),
                                grupo_contratacao_codigo=item.get("grupoContratacaoCodigo"),
                                grupo_contratacao_nome=item.get("grupoContratacaoNome"),
                                classificacao_superior_codigo=item.get("classificacaoSuperiorCodigo"),
                                classificacao_superior_nome=item.get("classificacaoSuperiorNome"),
                                unidade_fornecimento=item.get("unidadeFornecimento"),
                                valor_unitario=item.get("valorUnitario", 0),
                                valor_orcamento_exercicio=item.get("valorOrcamentoExercicio", 0),
                                data_desejada=data_desejada,
                                categoria_item_pca_nome=item.get("categoriaItemPcaNome"),
                                classificacao_catalogo_id=item.get("classificacaoCatalogoId", 0),
                                nomeUnidade=pca.get("nomeUnidade")
                            )
                            items_list.append(pca_item)
                            # mantenha um buffer para escrita em disco a cada 1000 itens
                            buffer.append(pca_item)

                if salvar_arquivo:
                    # Escreve em disco em modo append quando o buffer atingir 1000 itens
                    if len(buffer) >= 1000:
                        with open("itens.json", "a", encoding="utf-8") as f:
                            json.dump(
                                [item.__dict__ for item in buffer],
                                f,
                                ensure_ascii=False,
                                indent=2,
                                default=str  # converte datetime/date para string
                            )
                            f.write("\n")
                        print(f"✅ Gravados {len(buffer)} itens em itens.json (append). Limpeza do buffer.")
                        buffer.clear()

                    # Optionally, append raw API response for debugging
                    with open("pncp_response.json", "a", encoding="utf-8") as f:
                        json.dump(data, f, ensure_ascii=False, indent=4)
                        f.write("\n")

                    print("✅ Response appended to pncp_response.json")

                print(f"Created {len(items_list)} PCA Items.")
            else:
                print(f"❌ Failed to get data: {response.status_code}")
            if (len(items_list) >= max_items):
                pagina = maxPagina + 1
                break
            else:
                print(len(items_list), " items coletados ate o momento...")
        if (len(items_list) >= max_items):
            pagina = maxPagina + 1
            break
        else:
            print(len(items_list), " items coletados ate o momento...")
    
    print("Requisição à API do PNCP concluída.")
    # Ao final, grava qualquer item restante no buffer
    if salvar_arquivo and len(buffer) > 0:
        with open("itens.json", "a", encoding="utf-8") as f:
            json.dump(
                [item.__dict__ for item in buffer],
                f,
                ensure_ascii=False,
                indent=2,
                default=str
            )
            f.write("\n")
        print(f"✅ Gravados {len(buffer)} itens restantes em itens.json (append).")
        buffer.clear()

    return items_list