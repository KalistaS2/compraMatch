# ComprasMatch

Sistema para análise de similaridade de itens de compras públicas do PNCP (Portal Nacional de Contratações Públicas).

## Funcionalidades

- Busca de itens da API do PNCP
- Cálculo de similaridade entre itens usando embeddings (EmbeddingGemma)
- Visualização de grafos de similaridade
- Interface web para navegação de itens e similaridades

## Como Rodar

1. Instale as dependências: `pip install -r requirements.txt`
2. Configure o Kaggle API: Baixe o arquivo kaggle.json do seu perfil no Kaggle e coloque na raiz do projeto.
3. Execute `python api/tools.py` Para importar os dados (necessario para a aplicação)
4. Execute: `python run.py` Para iniciar a aplicação

## Dependências

- requests: Para requisições à API
- sentence-transformers: Para embeddings
- kagglehub: Para acesso ao modelo EmbeddingGemma
- networkx: Para grafos
- flask: Framework web
- scikit-learn: Para cálculos de similaridade

## API do PNCP

https://pncp.gov.br/api/consulta/swagger-ui/index.html#/Plano%20de%20Contrata%C3%A7%C3%A3o/consultarItensPorAno

## Versão

0.1

## Notas

- Necessário conta no Kaggle autenticada para acessar o EmbeddingGemma.
