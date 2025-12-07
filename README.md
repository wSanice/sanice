# ds_flow

> **Data Science Ágil e Fluente.** Do Excel ao Machine Learning em poucas linhas de código.

![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-Apache%202.0-blue)
![Status](https://img.shields.io/badge/status-stable-brightgreen)

O **ds_flow** é um wrapper Pythonic projetado para acelerar o dia a dia de Cientistas de Dados. Ele abstrai a complexidade do Pandas, Seaborn e Scikit-Learn em uma interface fluente (Method Chaining), permitindo que você foque na lógica de negócio, não na sintaxe.

---

## Instalação

```bash
pip install ds_flow
```

*(Ou, se estiver usando localmente, clone o repositório e rode `pip install -e .`)*

---

## Quick Start

Como transformar um CSV sujo em um modelo de Inteligência Artificial salvo em disco:

```python
from ds_flow import DataFlow

(DataFlow("vendas_sujas.xlsx")
    .sanitizar_colunas()                     # Padroniza: 'Data Venda' -> 'data_venda'
    .remover_nulos()                         # Remove linhas vazias
    .converter_data("data_venda")            # String -> Datetime
    .criar_coluna("dia_semana", lambda r: r['data_venda'].day_name())
    .filtrar("valor > 100")                  # Filtro estilo SQL
    .plotar("barras", x="dia_semana", y="valor", titulo="Vendas por Dia")
    .auto_ml(                                # Treina e Salva IA
        alvo="cliente_comprou", 
        tipo="classificacao", 
        salvar_modelo="minha_ia.pkl"
    )
)
```

---

## Funcionalidades Principais

### 1. Limpeza e Preparação (Data Cleaning)
Chega de sofrer com nomes de colunas com acentos ou espaços.
* **.sanitizar_colunas()**: Transforma `Preço (R$)` em `preco_r`.
* **.limpar_texto(col)**: Remove espaços extras e padroniza Maiúsculas.
* **.remover_nulos()**: Estratégias para apagar ou preencher com zeros.
* **.converter_data()**: Converte strings para objetos de data reais.

### 2. Manipulação (Wrangling)
* **.filtrar("coluna > valor")**: Sintaxe limpa e direta.
* **.criar_coluna("novo", logica)**: Aceita fórmulas matemáticas ou funções lambda complexas.
* **.unir(outro_df, chaves)**: Realiza Joins (Vlookup) entre tabelas facilmente.

### 3. Visualização (Plotting)
Wrapper automático para gráficos modernos (Seaborn):
* Tipos suportados: `barras`, `linha`, `scatter`, `hist`, `box`.
* Exemplo: `.plotar("scatter", x="idade", y="salario", hue="cargo")`.

### 4. Auto Machine Learning (AutoML)
O método `.auto_ml()` é um pipeline completo:
1.  **Encoding:** Detecta colunas de texto (ex: "Categoria") e converte para números automaticamente (One-Hot Encoding).
2.  **Split & Treino:** Divide dados e treina (Random Forest).
3.  **Blindagem:** Salva o modelo junto com a lista de colunas usadas, evitando erros futuros em produção.

### 5. Produção e Inferência
Use seus modelos salvos em dados novos sem quebrar o código.
* **.carregar_ia("modelo.pkl")**: Carrega o cérebro da IA.
* **.prever("nome_saida")**: Gera previsões alinhando as colunas automaticamente (se faltar coluna no dado novo, ele preenche; se sobrar, ele ignora).

---

## Exemplos de Uso

### Cenário A: Análise Exploratória Rápida

```python
from ds_flow import DataFlow

df = (DataFlow("clientes.csv")
    .sanitizar_colunas()
    .filtrar("idade >= 18 and estado == 'SP'")
    .ordenar("renda", ascendente=False)
    .resumo_estatistico() # Mostra média, desvio padrão, etc.
    .plotar("hist", x="renda", titulo="Distribuição de Renda em SP")
)
```

### Cenário B: Engenharia de Dados (Joins e Exportação)

```python
# Carrega tabela de vendas e junta com tabela de produtos
fluxo_vendas = DataFlow("vendas_2024.parquet")
produtos = DataFlow("cad_produtos.csv")

(fluxo_vendas
    .unir(produtos, chaves="id_produto", como="left")
    .criar_coluna("total", "qtd * preco_unitario")
    .salvar("vendas_consolidadas.xlsx") # Exporta para Excel
)
```

### Cenário C: Produção (Previsão de Novos Dados)

Como usar a IA treinada ontem nos dados que chegaram hoje (mesmo que venham incompletos):

```python
(DataFlow("novos_clientes_hoje.csv")
    .sanitizar_colunas()
    # Carrega a IA salva anteriormente
    .carregar_ia("minha_ia.pkl")
    # Faz a previsão (alinha colunas automaticamente para não dar erro)
    .prever(nome_coluna_saida="probabilidade_compra")
    .salvar("lista_para_vendedores.xlsx")
)
```

---

## Autor
Desenvolvido por **wSanice**.