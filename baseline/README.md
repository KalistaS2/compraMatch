# Baseline - Projeto de Pesquisa para Artigo Científico

Sistema completo de validação e comparação de algoritmos de similaridade para itens de compras públicas.

---

## Descrição

Este projeto implementa um framework completo para avaliar a performance de modelos de similaridade semântica. Utiliza dados sintéticos para garantir controle sobre variáveis experimentais e reprodutibilidade dos resultados.

## Objetivo Principal

Servir como baseline para comparação de diferentes modelos de embeddings e algoritmos de similaridade, fornecendo métricas detalhadas para publicação científica.

---

## Componentes Principais

### 1. `construcao.py` - Orquestrador Principal

Script que gerencia todo o pipeline de geração e avaliação:

```python
criar_itens()           # Gera combinações de produtos
processar_itens()       # Calcula baseline de similaridade  
comparar_arrays()       # Compara baseline com Gemma e calcula métricas
```

**Etapas de Execução:**
- **Etapa 1**: Lê `itensSinteticos.json` e cria todas as combinações possíveis de produtos com suas características
- **Etapa 2**: Processa itens e gera matriz de similaridade baseline (simples: 0 ou 1)
- **Etapa 3**: Compara resultados com modelo Gemma e calcula métricas de performance

### 2. `similaridadeBase.py` - Gerador de Embeddings

Calcula similaridades usando o modelo EmbeddingGemma:

**Funcionalidades:**
- Download automático do modelo via Kaggle
- Geração de embeddings para todos os itens
- Cálculo de matriz de similaridade com cosseno
- Aplicação de threshold configurável
- Salvamento de resultados em JSON

**Função Principal:**
```python
def similaridades_baseline(similaridade_min=0.7, salvar_json=True):
    # Carrega itens complexos
    # Faz login no Kaggle
    # Baixa modelo EmbeddingGemma
    # Gera embeddings
    # Calcula similaridades
    # Salva resultados
```

---

## Fluxo de Dados

```
itensSinteticos.json
        ↓
   [construcao.py]
        ↓
itens_complexos.json (todas as combinações)
        ↓
   [similaridadeBase.py]
        ↓
array_similaridade_base.json (0 ou 1)
array_similaridade_gemma_*.json (scores 0-1)
        ↓
   [comparar_arrays()]
        ↓
Métricas de Performance
(Acurácia, Precisão, Recall, F1, MAE, RMSE)
```

---

## Como Executar

### Requisitos

```bash
pip install -r ../requirements.txt
```

Necessário arquivo `kaggle.json` na raiz do projeto (obter em https://www.kaggle.com/settings/account)

### Execução

```bash
cd baseline
python construcao.py
```

A execução é dividida em 3 etapas com progresso exibido em tempo real.

---

## Estrutura de Dados

### Entrada: `json/itensSinteticos.json`

Formato hierárquico de categorias → itens → características:

```json
{
  "licitacoes_publicas": {
    "medicamentos_e_insumos_hospitalares": {
      "Dipirona Monoidratada": {
        "cor_da_embalagem_secundaria": ["Branco e Azul", "Amarelo e Vermelho"],
        "layout_do_rotulo": ["Texto horizontal", "Texto vertical"],
        "tipo_de_lacre_da_ampola": ["Plástico", "Anel de quebra"]
      },
      "Soro Fisiológico": { ... }
    }
  }
}
```

### Saída: `json/itens_complexos.json`

Todas as combinações geradas (explosão combinatória):

```json
{
  "itens": [
    {
      "classe_item": "medicamentos_e_insumos_hospitalares",
      "nome_item": "Dipirona Monoidratada Branco e Azul Texto horizontal Plástico"
    },
    {
      "classe_item": "medicamentos_e_insumos_hospitalares",
      "nome_item": "Dipirona Monoidratada Branco e Azul Texto horizontal Anel de quebra"
    }
    // ... todas as combinações
  ]
}
```

### Matriz de Similaridade Base: `json/array_similaridade_complexos.json`

```json
{
  "total_itens": 1000,
  "itens": [
    {
      "indice": 0,
      "item": "Dipirona Monoidratada Branco e Azul Texto horizontal Plástico",
      "classe": "medicamentos_e_insumos_hospitalares",
      "primeira_palavra": "Dipirona",
      "similaridade": [
        {"indice": 0, "item": "...", "similar": 1},
        {"indice": 1, "item": "...", "similar": 1},
        {"indice": 2, "item": "...", "similar": 0}
        // ...
      ]
    }
    // ... todos os itens
  ]
}
```

### Resultado Gemma: `json/array_similaridade_gemma_*.json`

Contém scores de confiança (0.0 a 1.0):

```json
{
  "total_itens": 1000,
  "itens": [
    {
      "indice": 0,
      "item": "Dipirona Monoidratada ...",
      "similaridade": [
        {"indice": 0, "item": "...", "similaridade": 0.9987},
        {"indice": 1, "item": "...", "similaridade": 0.8765},
        {"indice": 2, "item": "...", "similaridade": 0.1234}
        // ...
      ]
    }
    // ... todos os itens
  ]
}
```

---

## Métricas de Avaliação Calculadas

### Matriz de Confusão (Binary Classification)

| | Baseline=1 | Baseline=0 |
|---------|---------|---------|
| **Gemma≥threshold=1** | VP | FP |
| **Gemma<threshold=0** | FN | VN |

### Métricas de Performance

| Métrica | Fórmula | Interpretação |
|---------|---------|---------|
| **Acurácia** | (VP + VN) / Total | Taxa geral de acertos |
| **Precisão** | VP / (VP + FP) | De quantos similares preditos, quantos eram corretos |
| **Recall/Sensibilidade** | VP / (VP + FN) | De quantos similares reais, quantos foram detectados |
| **Especificidade** | VN / (VN + FP) | Taxa de detecção correta de não-similares |
| **F1-Score** | 2 × (Precisão × Recall) / (Precisão + Recall) | Média harmônica |
| **MAE** | Σ\|Y_true - Y_pred\| / n | Erro médio absoluto |
| **RMSE** | √(Σ(Y_true - Y_pred)² / n) | Raiz do erro quadrático médio |

---

## Parâmetros Configuráveis

### Em `construcao.py`

```python
# Threshold para comparação Gemma
comparar_arrays(threshold=0.7)  # Pode ser 0.7 ou 0.9
```

### Em `similaridadeBase.py`

```python
def similaridades_baseline(similaridade_min=0.7, salvar_json=True):
    # similaridade_min: threshold para salvar similaridades
    # salvar_json: se True, salva em arquivo
```

---

## Interpretação dos Resultados

### Cenário Ideal

- Acurácia: 0.95+
- Precisão: 0.90+
- Recall: 0.90+
- F1-Score: 0.90+

### Indicadores de Problema

- **Baixa Precisão + Alto Recall**: Modelo muito permissivo, muitos falsos positivos
- **Alta Precisão + Baixo Recall**: Modelo muito restritivo, perde muitos positivos
- **Alto MAE**: Scores de confiança descalibrados
- **Alto RMSE**: Presença de outliers nas predições

---

## Exemplos de Uso

### Executar Pipeline Completo

```bash
python construcao.py
```

### Apenas Criar Itens Complexos

```python
from construcao import criar_itens
criar_itens()
```

### Apenas Processar e Gerar Baseline

```python
from construcao import processar_itens
processar_itens()
```

### Apenas Comparar Resultados

```python
from construcao import comparar_arrays
resultados = comparar_arrays(threshold=0.7)
print(f"Acurácia: {resultados['acuracia']:.4f}")
print(f"F1-Score: {resultados['f1']:.4f}")
```

---

## Reprodutibilidade

Para garantir reprodutibilidade dos experimentos:

1. **Use dados sintéticos fixos** - `itensSinteticos.json` é controlado
2. **Registre a versão do modelo** - EmbeddingGemma é baixado do Kaggle
3. **Documente o threshold** - Padrão: 0.7 e 0.9
4. **Salve todos os arrays** - Mantenha cópias dos JSON gerados
5. **Registre timestamp** - Adicione ao nome do arquivo

---

## Próximos Passos

1. Testar com diferentes thresholds (0.5, 0.6, 0.7, 0.8, 0.9)
2. Comparar com outros modelos de embedding
3. Experimentar com diferentes funções de similaridade (cosseno, euclidiana, etc)
4. Gerar gráficos de ROC e Precision-Recall
5. Fazer análise de sensibilidade dos parâmetros

---

## Autores e Contribuições

Projeto de pesquisa para validação de algoritmos de similaridade em compras públicas.

## Versão

- v0.1 - Alpha (Prototipagem)
