# CompraMatch

Sistema para análise de similaridade de itens de compras públicas e pesquisa de validação de algoritmos de matching.

---

## Estrutura do Projeto

Este repositório contém dois componentes principais:

1. **CompraMatch** - Sistema principal de análise de similaridade (aplicação web)
2. **Baseline** - Projeto de pesquisa para validação e comparação de algoritmos de similaridade

---

## CompraMatch - Aplicação Principal

Sistema web para análise de similaridade de itens de compras públicas do PNCP (Portal Nacional de Contratações Públicas).

### Funcionalidades

- 🔍 Busca de itens da API do PNCP
- 📊 Cálculo de similaridade entre itens usando embeddings (EmbeddingGemma)
- 🌐 Visualização de grafos de similaridade
- 💻 Interface web para navegação interativa de itens e similaridades

### Instalação e Configuração

1. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure a autenticação Kaggle:**
   - Baixe o arquivo `kaggle.json` do seu perfil no [Kaggle](https://www.kaggle.com/settings/account)
   - Coloque o arquivo na raiz do projeto

3. **Importe os dados (primeira execução):**
   ```bash
   python api/tools.py
   ```

4. **Inicie a aplicação web:**
   ```bash
   python run.py
   ```
   
   A aplicação estará disponível em: `http://127.0.0.1:5000`

### Estrutura de Diretórios

```
api/                    # Backend - APIs e lógica de negócio
  ├── app.py           # Aplicação Flask principal
  ├── tools.py         # Ferramentas para importação de dados
  ├── orgaos.py        # Extractores de órgãos públicos
  ├── similaridades.py # Cálculos de similaridade
  └── model/           # Modelos de dados
templates/             # Templates HTML
static/                # Arquivos CSS, JavaScript
json/                  # Dados em JSON
itens.json            # Cache de itens
grafo_*.gpickle       # Grafos de similaridade (diferentes thresholds)
```

### Dependências Principais

- **requests** - Requisições HTTP à API PNCP
- **sentence-transformers** - Modelos de embedding para similaridade semântica
- **kagglehub** - Acesso ao modelo EmbeddingGemma do Kaggle
- **networkx** - Manipulação e análise de grafos
- **flask** - Framework web
- **scikit-learn** - Utilitários para cálculos de similaridade

---

## Baseline - Projeto de Pesquisa

Projeto separado dedicado à validação e comparação de algoritmos de similaridade para produção de artigo científico.

### Objetivo

Criar um baseline para avaliar a performance de diferentes modelos de similaridade (ex: EmbeddingGemma) comparando com:
- Métricas de classificação (VP, FP, VN, FN)
- Acurácia, Precisão, Recall, F1-Score
- Erro Médio Absoluto (MAE)
- Raiz do Erro Quadrático Médio (RMSE)

### Funcionalidades

- ✅ Geração de itens sintéticos com múltiplas características
- 📐 Criação de combinações de produtos para teste
- 🧮 Cálculo de baseline de similaridade
- 📊 Comparação de resultados e análise de métricas
- 📈 Validação e avaliação de modelos

### Como Executar

1. **Navegue para o diretório baseline:**
   ```bash
   cd baseline
   ```

2. **Execute o script principal:**
   ```bash
   python construcao.py
   ```

   Este script executa 3 etapas:
   - **Etapa 1**: Criação de itens complexos a partir de `itensSinteticos.json`
   - **Etapa 2**: Processamento de itens e geração do baseline de similaridade
   - **Etapa 3**: Comparação entre baseline e resultados do Gemma

### Arquivo de Entrada

**`json/itensSinteticos.json`** - Define as categorias de itens e suas características:

```json
{
  "licitacoes_publicas": {
    "categoria": {
      "Item": {
        "caracteristica1": ["opção1", "opção2", ...],
        "caracteristica2": ["opção1", "opção2", ...],
        "caracteristica3": ["opção1", "opção2", ...]
      }
    }
  }
}
```

### Arquivos Gerados

- `json/itens_complexos.json` - Todas as combinações de itens geradas
- `json/array_similaridade_complexos.json` - Baseline de similaridade (simples: 0 ou 1)
- `json/array_similaridade_gemma_*.json` - Resultados do modelo Gemma com scores de confiança

### Scripts Principais

#### `construcao.py`

Orquestra todo o fluxo de construção e validação:

```python
criar_itens()           # Gera combinações de produtos
processar_itens()       # Calcula baseline de similaridade
comparar_arrays()       # Compara baseline com Gemma e calcula métricas
```

#### `similaridadeBase.py`

Calcula similaridades usando EmbeddingGemma:
- Gera embeddings dos itens
- Calcula matriz de similaridade
- Aplica threshold configurável
- Salva resultados em JSON

### Métricas de Avaliação

O baseline calcula:

| Métrica | Descrição |
|---------|-----------|
| **Acurácia** | (VP + VN) / Total |
| **Precisão** | VP / (VP + FP) |
| **Recall** | VP / (VP + FN) |
| **F1-Score** | Média harmônica de Precisão e Recall |
| **MAE** | Média do erro absoluto entre scores |
| **RMSE** | Raiz da média dos erros quadráticos |
| **Sensibilidade** | VP / (VP + FN) - Taxa de detecção de similares |
| **Especificidade** | VN / (VN + FP) - Taxa de detecção de não-similares |

---

## Configuração Geral

### Dependências do Projeto

Todas as dependências estão em `requirements.txt`:
- requests
- sentence-transformers
- kagglehub
- networkx
- flask
- scikit-learn

### Autenticação Kaggle

É necessária uma conta autenticada no Kaggle para acessar o modelo EmbeddingGemma:
1. Acesse https://www.kaggle.com/settings/account
2. Baixe a chave API
3. Coloque o arquivo `kaggle.json` na raiz do projeto

---

## API PNCP (Portal Nacional de Contratações Públicas)

Documentação da API utilizada:
https://pncp.gov.br/api/consulta/swagger-ui/index.html#/Plano%20de%20Contrata%C3%A7%C3%A3o/consultarItensPorAno

---

## Versão

- v0.1 - Alpha

---

## Notas Importantes

- A autenticação Kaggle é obrigatória para usar EmbeddingGemma em ambos os projetos
- O baseline utiliza dados sintéticos para controlar variáveis e garantir reprodutibilidade
- Recomenda-se usar o baseline antes de aplicar em dados reais do PNCP
