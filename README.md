# ComprasMatch 

intalar as dependencias
- Requests
utilizado para fazer as requisições da Api
pip intsall requests

- SpaCy
utilizado para fazer tratamento de NLP e calculo de similaridade
pip install spacy

- EmbeddingGemma
utilizado para criar os embeddings e fazer o calculo de similaridade
!pip install git+https://github.com/huggingface/transformers@v4.56.0-Embedding-Gemma-preview

e instalar a o pacote para tratar de lingua portuguesa com precisão
python -m spacy download pt_core_news_lg

"# API dos PNCP"
https://pncp.gov.br/api/consulta/swagger-ui/index.html#/Plano%20de%20Contrata%C3%A7%C3%A3o/consultarItensPorAno


# versionamento - 0.1
utilização do modelo EmbeddingGemma via biblioteca *kagglehub* para fazer os os embenddings e o calculo de similaridade
- Nota:
precisa ter conta autenticada no kaggle para autenticar no codigo, site para criar a conta e aceitar os termos para ter acesso ao EmbeddingGemma acessar o link: https://www.kaggle.com/models/google/embeddinggemma, apos criar a conta e aceitar os termos, ir em account e gerar um API token, isso vai baixar um arquivo com o seu user e token que serão utilizados na aplicação

a biblioteca SpaCy se mostrou ineficiente devido a fazer a similaridade apenas semantica