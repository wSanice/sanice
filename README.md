<div align="center">

<p align="center">
  <img src="https://raw.githubusercontent.com/wSanice/sanice/refs/heads/main/assets/sanice.png" alt="Sanice Banner" width="100%"/>
</p>

> (Sistema Automatizado de Normalização, Inteligência Computacional e Estatística)<br>
> (System for Automated Normalization, Intelligence, Computation, and Statistics)



![Python Version](https://img.shields.io/badge/python-3.8%2B-blue)
![License](https://img.shields.io/badge/license-Apache%202.0-blue)
![Status](https://img.shields.io/badge/status-stable-brightgreen)

[🇺🇸 English](#-english) | [🇧🇷 Português](#-português) | [🇨🇳 &nbsp; 🇮🇳 &nbsp;Multi-language](#-Multilanguage)

</div>

---
<details>
<summary><b>Release v1.0.5: Architecture Refactoring & Encapsulation</b></summary>
<br>

This version focuses on improving Code Quality and the library's internal architecture, in addition to important documentation fixes.

### Architectural Changes (Encapsulation)
We refactored the library core (`core.py`) to follow Object-Oriented Programming best practices:
* **Constant Encapsulation:** The `I18N` (translations) and `METHOD_ALIASES` (method aliases) dictionaries were moved from the global scope to inside the `Sanice` class.
* **Clean Namespace:** Avoids global scope "pollution" when importing the library, preventing conflicts with other libs.
* **Instance Access:** All internal methods now access configurations via `self.I18N` and `self.METHOD_ALIASES`, facilitating future inheritance and class extension.

### Documentation
* **Extras Installation:** The `README.md` has been updated to include the correct installation instruction for those who wish to use the API:
  ```bash
  pip install "sanice[api]"
  ```
</details>

<a name="-english"></a>
## 🇺🇸 English

**Sanice** is a fluent Python wrapper designed to accelerate Data Science workflows. It abstracts the complexity of Pandas, Scikit-Learn, and FastAPI into a method-chaining interface, allowing you to focus on business logic rather than syntax.

### Installation

**Standard Installation (Data Science Core):**
```bash
pip install sanice
```
### Full Installation (includes API support):
**Required if you plan to use** `.serve_api()`
```bash
pip install "sanice[api]"
```
### CLI Helper
You can verify installed commands directly from your terminal without opening Python:

```bash
sanice help    # 🇺🇸 English
sanice bangzhu # 🇨🇳 Chinese
sanice madad   # 🇮🇳 Hindi
```
### ⚡ Quick Start

**How to turn a dirty CSV into a deployed AI model in minutes.**

```python
from sanice import Sanice

(Sanice("raw_data.csv")
    .fix_columns()                    # Standardize names to snake_case
    .transform("price", "money")      # Cleans money format ("$ 1,000.00" -> 1000.0)
    .drop_nulls()                     # Removes empty rows
    .create_column("total", "price * qty")
    .handle_outliers("total")         # Removes statistical anomalies (IQR)
    .auto_ml(                         # Trains Random Forest & saves model
        target="sold", 
        type="classification", 
        save_path="my_model.pkl"
    )
    .serve_api()                      # Deploys a REST API on localhost:8000
)
```

### Snippets & Command Reference

Here is the complete list of available methods organized by category.

#### 1. Cleaning & ETL
| Command | Description |
| :--- | :--- |
| `app.fix_columns()` | Converts all column names to `snake_case`. |
| `app.transform(col, rule)` | Applies logic: `'money'`, `'digits'`, `'email'`, `'upper'`, `'lower'`. |
| `app.drop_nulls(strategy, val)` | Strategy: `'drop'` or `'fill'`. |
| `app.clean_text([cols])` | Strips spaces and converts text to Title Case. |
| `app.convert_date(col, fmt)` | Converts a string column to datetime objects. |

> **Use Cases:**
> * Standardization of data extracted from legacy systems or unformatted Excel sheets.
> * Rapid conversion of currency strings to float before calculations.
> * Preparation of web form data where users input dates in various formats.

**Application Example:**
```python
# Cleaning a messy HR dataset
(Sanice("raw_employees.csv")
    .fix_columns()                    # "Emp Name" -> "emp_name"
    .clean_text(["emp_name", "dept"])
    .transform("salary", "money")     # "$ 2,500.00" -> 2500.0
    .convert_date("hire_date")        # String -> Datetime
)
```

#### 2. Data Manipulation
| Command | Description |
| :--- | :--- |
| `app.create_column(name, logic)` | Creates a column using a string expression or lambda. |
| `app.filter(query)` | Filters rows using SQL-like syntax (e.g., `"age > 18"`). |
| `app.sort(col, ascending)` | Sorts the dataset by a specific column. |
| `app.join(other_df, keys, how)` | Merges two datasets (Left, Right, Inner, Outer). |
| `app.group([cols], val, op)` | Groups data and calculates sum, mean, or count. |
| `app.pivot_table(idx, col, val)` | Creates a Pivot Table from the data. |

> **Use Cases:**
> * Feature Engineering (e.g., creating "average ticket" or "days since last purchase").
> * Merging "Sales" and "Customers" tables to enrich the dataset (VLOOKUP/JOIN).
> * Customer segmentation for specific marketing campaigns.

**Application Example:**
```python
# Total Sales Analysis by Region
(Sanice("sales.csv")
    .filter("status == 'Completed'")
    .create_column("revenue", "price * quantity")
    .group(
        cols=["region", "category"], 
        value_col="revenue", 
        operation="sum"
    )
    .sort("revenue", ascending=False)
)
```

#### 3. Analytics & Visualization
| Command | Description |
| :--- | :--- |
| `app.describe()` | Displays mean, std, min, max, and percentiles. |
| `app.correlation_matrix()` | Plots a heatmap of correlations between numeric vars. |
| `app.handle_outliers([cols])` | Removes outliers automatically using the IQR method. |
| `app.plot(type, x, y, hue)` | Plots charts: `'bar'`, `'line'`, `'scatter'`, `'hist'`, `'box'`. |

> **Use Cases:**
> * Exploratory Data Analysis (EDA) to understand data profiles before modeling.
> * Visual identification of variables that influence the target result (correlation).
> * Detection and removal of anomalies (e.g., negative ages or exorbitant prices).

**Application Example:**
```python
# Rapid Dataset Diagnosis
(Sanice("biological_data.csv")
    .describe()
    .handle_outliers(["age", "glucose"]) # Remove anomalies
    .correlation_matrix()                # Shows influence factors
    .plot("scatter", x="age", y="glucose", hue="diagnosis")
)
```

#### 4. AI & Machine Learning
| Command | Description |
| :--- | :--- |
| `app.scale(method)` | Normalizes data using `'minmax'` or `'standard'` scaler. |
| `app.auto_ml(target, type, path)` | AutoML pipeline: encodes, splits, trains, and saves model. |
| `app.load_ai(path)` | Loads a pre-trained `.pkl` model into memory. |
| `app.predict(output_col)` | Generates predictions using the loaded model. |

> **Use Cases:**
> * Quick creation of baselines to validate business hypotheses.
> * Churn Prediction (customers likely to cancel) or Credit Scoring.
> * Demand forecasting based on sales history (Regression).

**Application Example:**
```python
# Training and using a Churn prediction model
(Sanice("telecom_churn.csv")
    .scale("minmax")
    .auto_ml(target="churn", type="classification", save_path="my_ai.pkl")
)

# ... In another script, loading and predicting:
(Sanice("new_customers.csv")
    .load_ai("my_ai.pkl")
    .predict(output_col="churn_prob")
)
```

#### 5. Export & Deployment
| Command | Description |
| :--- | :--- |
| `app.save(path)` | Exports data to `.csv`, `.xlsx`, or `.parquet`. |
| `app.export_sql(url, table)` | Pushes the dataframe to a SQL database. |
| `app.serve_api()` | Starts a FastAPI server to serve predictions. |

> **Use Cases:**
> * Exporting treated data (Bronze -> Silver) to BI tools like Power BI or Tableau.
> * Instant creation of AI microservices for Mobile or Web App integration.
> * Persistence of clean data into relational databases (PostgreSQL/MySQL).

**Application Example:**
```python
# Final Pipeline: Clean -> Save Parquet -> Deploy API
(Sanice("raw_data.csv")
    .fix_columns()
    .auto_ml("target", "regression", "model.pkl")
    .save("clean_data.parquet")   # Data Backup
    .serve_api()                  # API Online at http://localhost:8000
)
```

### License

This project is licensed under the Apache License, Version 2.0. See the [LICENSE](https://www.apache.org/licenses/LICENSE-2.0)  for details.

<br>

---

<details>
<summary><b>Atualização v1.0.5: Refatoração de Arquitetura & Encapsulamento</b></summary>
<br>

Esta versão foca na melhoria da qualidade do código (Code Quality) e na arquitetura interna da biblioteca, além de correções importantes na documentação.

### Mudanças Arquiteturais (Encapsulamento)
Refatoramos o núcleo da biblioteca (`core.py`) para seguir melhores práticas de Programação Orientada a Objetos:
* **Encapsulamento de Constantes:** Os dicionários `I18N` (traduções) e `METHOD_ALIASES` (apelidos de métodos) foram movidos do escopo global para dentro da classe `Sanice`.
* **Namespace Limpo:** Evita "poluição" do escopo global ao importar a biblioteca, prevenindo conflitos com outras libs.
* **Acesso via Instância:** Todos os métodos internos agora acessam configurações via `self.I18N` e `self.METHOD_ALIASES`, facilitando futura herança e extensão da classe.

### Documentação
* **Instalação de Extras:** O `README.md` foi atualizado para incluir a instrução correta de instalação para quem deseja usar a API:
  ```bash
  pip install "sanice[api]"
  ```
</details>

<a name="-português"></a>
## 🇧🇷 Português

**Sanice** é um wrapper Python fluido projetado para acelerar fluxos de trabalho de Data Science. Ele abstrai a complexidade do Pandas, Scikit-Learn e FastAPI em uma interface de encadeamento de métodos (method-chaining), permitindo que você foque na lógica de negócios em vez da sintaxe.

### Instalação

**Instalação Padrão (Núcleo Data Science):**
```bash
pip install sanice
```
### Instalação Completa (inclui suporte a API): 
**Necessário se você planeja usar** `.servir_api()`
```bash
pip install "sanice[api]"
```


### Ajuda no Terminal (CLI)

Você pode verificar os comandos disponíveis direto do seu terminal, sem abrir o Python:

```bash
sanice ajuda   # 🇧🇷 Português
```

### ⚡ Início Rápido

**Como transformar um CSV sujo em um modelo de IA em produção em minutos.**

```python
from sanice import Sanice

(Sanice("raw_data.csv")
    .corrigir_colunas()               # Padroniza nomes para snake_case
    .transformar("price", "dinheiro") # Limpa formato monetário ("R$ 1.000,00" -> 1000.0)
    .remover_nulos()                  # Remove linhas vazias
    .criar_coluna("total", "price * qty")
    .tratar_outliers("total")         # Remove anomalias estatísticas (IQR)
    .auto_ml(                         # Treina Random Forest & salva modelo
        alvo="sold", 
        tipo="classificacao", 
        salvar_modelo="my_model.pkl"
    )
    .servir_api()                     # Sobe uma API REST em localhost:8000
)
```

### Snippets e Referência de Comandos

Aqui está a lista completa de métodos disponíveis organizados por categoria.

#### 1. Limpeza e ETL
| Comando | Descrição |
| :--- | :--- |
| `app.corrigir_colunas()` | Converte todos os nomes de colunas para `snake_case`. |
| `app.transformar(col, rule)` | Aplica lógica: `'dinheiro'`, `'numeros'`, `'email'`, `'upper'`, `'lower'`. |
| `app.remover_nulos(strategy, val)` | Estratégia: `'apagar'` (drop) ou `'preencher'` (fill). |
| `app.limpar_texto([cols])` | Remove espaços extras e converte texto para Title Case. |
| `app.converter_data(col, fmt)` | Converte uma coluna de string para objetos datetime. |

> **Casos de Uso:**
> * Padronização de dados extraídos de sistemas legados ou planilhas Excel desformatadas.
> * Conversão rápida de colunas de moeda brasileira (R$) para float antes de cálculos.
> * Preparação de dados de formulários web onde usuários inserem datas em formatos variados.

**Exemplo de Aplicação:**
```python
# Limpeza de uma base de RH desorganizada
(Sanice("funcionarios_bruto.csv")
    .corrigir_colunas()                 # "Nome Func" -> "nome_func"
    .limpar_texto(["nome_func", "setor"])
    .transformar("salario", "dinheiro") # "R$ 2.500,00" -> 2500.0
    .converter_data("data_admissao")    # String -> Datetime
)
```

#### 2. Manipulação de Dados
| Comando | Descrição |
| :--- | :--- |
| `app.criar_coluna(name, logic)` | Cria uma coluna usando expressão string ou lambda. |
| `app.filtrar(query)` | Filtra linhas usando sintaxe estilo SQL (ex: `"age > 18"`). |
| `app.ordenar(col, ascending)` | Ordena o dataset por uma coluna específica. |
| `app.unir(other_df, keys, how)` | Une dois datasets (Left, Right, Inner, Outer). |
| `app.agrupar([cols], val, op)` | Agrupa dados e calcula soma, média ou contagem. |
| `app.tabela_dinamica(idx, col, val)` | Cria uma Tabela Dinâmica a partir dos dados. |

> **Casos de Uso:**
> * Criação de Features (Feature Engineering) como "ticket médio" ou "dias desde a última compra".
> * Unificação de tabelas de "Vendas" e "Clientes" para enriquecer o dataset (VLOOKUP/JOIN).
> * Segmentação de base de clientes para campanhas de marketing específicas.

**Exemplo de Aplicação:**
```python
# Análise de Vendas Totais por Região
(Sanice("vendas.csv")
    .filtrar("status == 'Concluido'")
    .criar_coluna("faturamento", "preco * quantidade")
    .agrupar(
        cols=["regiao", "categoria"], 
        value_col="faturamento", 
        operacao="soma"
    )
    .ordenar("faturamento", ascendente=False)
)
```

#### 3. Análise e Visualização
| Comando | Descrição |
| :--- | :--- |
| `app.resumo_estatistico()` | Exibe média, desvio padrão, min, max e percentis. |
| `app.matriz_correlacao()` | Plota um mapa de calor das correlações entre vars numéricas. |
| `app.tratar_outliers([cols])` | Remove outliers automaticamente usando o método IQR. |
| `app.plotar(type, x, y, hue)` | Plota gráficos: `'bar'`, `'line'`, `'scatter'`, `'hist'`, `'box'`. |

> **Casos de Uso:**
> * Análise Exploratória de Dados (EDA) para entender o perfil dos dados antes da modelagem.
> * Identificação visual de variáveis que influenciam o resultado desejado (correlação).
> * Detecção e remoção de anomalias (ex: idades negativas ou preços exorbitantes).

**Exemplo de Aplicação:**
```python
# Diagnóstico rápido de dataset
(Sanice("dados_biologicos.csv")
    .resumo_estatistico()
    .tratar_outliers(["idade", "glicose"]) # Remove anomalias
    .matriz_correlacao()                   # Mostra o que influencia o que
    .plotar("scatter", x="idade", y="glicose", hue="diagnostico")
)
```

#### 4. IA e Machine Learning
| Comando | Descrição |
| :--- | :--- |
| `app.escalonar(method)` | Normaliza dados usando escalonador `'minmax'` ou `'standard'`. |
| `app.auto_ml(target, type, path)` | Pipeline AutoML: encode, split, treino e salvamento do modelo. |
| `app.carregar_ia(path)` | Carrega um modelo `.pkl` pré-treinado na memória. |
| `app.prever(output_col)` | Gera previsões usando o modelo carregado. |

> **Casos de Uso:**
> * Criação rápida de *baselines* (modelos de referência) para validar hipóteses.
> * Previsão de Churn (clientes que vão cancelar) ou Score de Crédito.
> * Previsão de demanda de estoque baseada em histórico de vendas.

**Exemplo de Aplicação:**
```python
# Treinando e usando um modelo de previsão de Churn
(Sanice("telecom_churn.csv")
    .escalonar("minmax")
    .auto_ml(alvo="churn", tipo="classificacao", salvar_modelo="meu_ia.pkl")
)

# ... Em outro script, carregando e prevendo:
(Sanice("novos_clientes.csv")
    .carregar_ia("meu_ia.pkl")
    .prever(output_col="probabilidade_churn")
)
```

#### 5. Exportação e Deploy
| Comando | Descrição |
| :--- | :--- |
| `app.salvar(path)` | Exporta dados para `.csv`, `.xlsx` ou `.parquet`. |
| `app.exportar_sql(url, table)` | Envia o dataframe para um banco de dados SQL. |
| `app.servir_api()` | Inicia um servidor FastAPI para servir previsões. |

> **Casos de Uso:**
> * Exportação de dados tratados para ferramentas de BI como Power BI.
> * Criação instantânea de microserviços de IA para integração com Apps.
> * Persistência de dados limpos em bancos relacionais (PostgreSQL/MySQL).

**Exemplo de Aplicação:**
```python
# Pipeline final: Limpa -> Salva Parquet -> Vira API
(Sanice("dados_brutos.csv")
    .corrigir_colunas()
    .auto_ml("target", "regressao", "modelo.pkl")
    .salvar("dados_limpos.parquet") # Backup dos dados
    .servir_api()                   # API Online em http://localhost:8000
)
```

---
<a name="-Multilanguage"></a>
### Multi-language Support / Suporte Multilíngue

Sanice is designed for global people. You can call methods in English, Portuguese, Chinese, or Hindi. <br>
*O Sanice foi projetado para equipes globais. Você pode chamar métodos em Inglês, Português, Chinês ou Hindi.*

<details>
<summary><b>CLICK HERE to see the full Command Translation Table / CLIQUE AQUI para ver a Tabela de Tradução</b></summary>
<br>

| 🇧🇷 PT-BR (Original) | 🇺🇸 English | 🇨🇳 Chinese (中文) | 🇮🇳 Hindi (Hinglish) |
| :--- | :--- | :--- | :--- |
| `corrigir_colunas` | `fix_columns` | `修正列名` | `column_sudhare` |
| `limpar_texto` | `clean_text` | `清洗文本` | `text_safai` |
| `remover_nulos` | `remove_nulls` | `移除空值` | `null_hataye` |
| `converter_data` | `convert_date` | `转换日期` | `date_badlo` |
| `criar_coluna` | `create_column` | `创建列` | `column_banaye` |
| `filtrar` | `filter_data` | `过滤数据` | `filter_kare` |
| `ordenar` | `sort_data` | `排序数据` | `sort_kare` |
| `unir` | `join_data` | `合并数据` | `jode` |
| `plotar` | `plot_chart` | `绘制图表` | `graph_banaye` |
| `resumo_estatistico` | `stats_summary` | `统计摘要` | `stats_dekhe` |
| `salvar` | `save_file` | `保存文件` | `save_kare` |
| `auto_ml` | `train_automl` | `自动训练` | `automl_kare` |
| `carregar_ia` | `load_ai` | `加载模型` | `ai_load_kare` |
| `prever` | `predict` | `预测` | `bhavishya_bataye` |
| `ver` | `view` | `查看` | `dekhe` |
| `ajuda` | `help` | `帮助` | `madad` |
| `agrupar` | `group_by` | `分组` | `samuh_banaye` |
| `tabela_dinamica` | `pivot_table` | `透视表` | `pivot_table` |
| `exportar_sql` | `export_sql` | `导出SQL` | `sql_export` |
| `matriz_correlacao` | `correlation_matrix` | `相关矩阵` | `sambandh_matrix` |
| `tratar_outliers` | `handle_outliers` | `处理异常值` | `outliers_hataye` |
| `escalonar` | `scale_data` | `数据缩放` | `scale_kare` |
| `servir_api` | `serve_api` | `启动API` | `api_chalu_kare` |
| `transformar` | `transform` | `数据转换` | `badlav_kare` |

</details>

### Licença

Este projeto está licenciado sob a Apache License, Version 2.0. Consulte a [LICENSE](https://www.apache.org/licenses/LICENSE-2.0)  para obter detalhes.

<div align="right">
    <a href="#sanice">⬆️ Back to Top</a>
</div>
<br><br>
<p align="center">
  <i>"Blind faith is the tool of monsters and fools. Analyze the data."</i>
</p>

---
Desenvolvido por **wSanice**.
