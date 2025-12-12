# CompraJunto - Sistema de Compras Compartilhadas

Uma aplicação web para visualizar e gerenciar compras compartilhadas entre diferentes órgãos públicos, com análise de similaridade de itens.

## 📋 Funcionalidades

- **Home**: Dashboard com estatísticas de órgãos, itens cadastrados e compras replicadas
- **Grafo de Similaridade**: Visualização interativa do grafo de similaridade entre itens (90% threshold)
- **Listagem de Itens**: Visualização e filtro dos itens cadastrados no sistema

## 🚀 Como Executar

### Pré-requisitos

- Python 3.8+
- Pip

### Instalação

1. Instale as dependências:

```bash
pip install -r dependencies.txt
```

### Execução

Na raiz do projeto, execute:

```bash
python run.py
```

Ou a partir do diretório `api`:

```bash
cd api
python pncpApi.py
```

A aplicação será iniciada em: **http://127.0.0.1:5000**

## 📁 Estrutura do Projeto

```
compraMatch/
├── api/
│   ├── app.py                 # Backend Flask
│   ├── pncpApi.py             # Script principal
│   ├── similaridades.py       # Cálculo de similaridades
│   ├── requisicaoApi.py       # Requisições à API PNCP
│   ├── orgaos.py              # Extração de órgãos
│   └── model/
│       └── items.py           # Modelo de dados
├── templates/
│   ├── home.html              # Página inicial (dashboard)
│   ├── grafo.html             # Página do grafo de similaridade
│   └── itens.html             # Página de listagem de itens
├── static/
│   ├── style.css              # Estilos CSS
│   ├── grafo.js               # Script do grafo (D3.js)
│   └── itens.js               # Script da listagem de itens
├── run.py                     # Script de inicialização
├── dependencies.txt           # Dependências do projeto
└── README.md                  # Este arquivo
```

## 🔧 Arquivos de Dados

A aplicação espera os seguintes arquivos na raiz do projeto:

- `itens.json` - Lista de itens cadastrados (fornecido por `pncpApi.py`)
- `grafo_Similaridade_90_porcento.gpickle` - Grafo de similaridade em formato pickle
- `matriz_Similaridade_90_porcento.json` - Matriz de similaridade em JSON

## 🎨 Tecnologias Utilizadas

- **Backend**: Flask (Python)
- **Frontend**: HTML5, CSS3, JavaScript
- **Visualização de Grafos**: D3.js
- **Análise de Dados**: NetworkX, SentenceTransformers, Scikit-learn

## 📊 Páginas

### Home (/)
- Exibe estatísticas do sistema
- Total de órgãos (usuários)
- Total de itens cadastrados
- Total de itens no grafo
- Total de compras replicadas (similaridade > 90%)
- Lista de compras ativas

### Grafo (/grafo)
- Visualização interativa do grafo de similaridade
- Nós representam itens/órgãos
- Arestas representam conexões de similaridade
- Controles de zoom (zoom in, zoom out, reset)
- Legenda de categorias

### Itens (/itens)
- Listagem completa de itens cadastrados
- Busca por nome/descrição
- Filtro por órgão
- Visualização de detalhes (quantidade, valor, data, etc.)

## 🔗 APIs Disponíveis

- `GET /api/orgaos` - Retorna lista de órgãos
- `GET /api/itens` - Retorna lista de itens
- `GET /api/grafo` - Retorna dados do grafo em formato JSON

## 📝 Notas

- A aplicação consome dados de `itens.json` e `grafo_Similaridade_90_porcento.gpickle`
- O grafo é visualizado usando D3.js com simulação de força
- Os dados são carregados via APIs REST do backend Flask
- A aplicação suporta filtros e buscas em tempo real

## 🤝 Contribuições

Este é um projeto de pesquisa. Sinta-se livre para contribuir!

## 📄 Licença

MIT License
