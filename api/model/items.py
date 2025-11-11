from dataclasses import dataclass
from datetime import datetime, date

@dataclass
class PcaItem:
    descricao_item: str
    nome_classificacao_catalogo: str
    quantidade_estimada: int
    pdm_codigo: str
    data_inclusao: datetime
    numero_item: int
    data_atualizacao: datetime
    valor_total: float
    pdm_descricao: str
    codigo_item: str
    unidade_requisitante: str
    grupo_contratacao_codigo: str
    grupo_contratacao_nome: str
    classificacao_superior_codigo: str
    classificacao_superior_nome: str
    unidade_fornecimento: str
    valor_unitario: float
    valor_orcamento_exercicio: float
    data_desejada: date
    categoria_item_pca_nome: str
    classificacao_catalogo_id: int
    nomeUnidade: str