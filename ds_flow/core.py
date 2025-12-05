# Arquivo: ds_flow/core.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import joblib  # Necessário para salvar e carregar o modelo de IA

class DataFlow:
    def __init__(self, fonte_dados):
        """
        Inicializa o fluxo. Aceita caminho de arquivo (csv, xlsx, parquet) ou DataFrame.
        """
        self.df = None
        try:
            if isinstance(fonte_dados, pd.DataFrame):
                self.df = fonte_dados.copy()
            elif isinstance(fonte_dados, str):
                if fonte_dados.endswith('.csv'):
                    self.df = pd.read_csv(fonte_dados)
                elif fonte_dados.endswith(('.xls', '.xlsx')):
                    self.df = pd.read_excel(fonte_dados)
                elif fonte_dados.endswith('.parquet'):
                    self.df = pd.read_parquet(fonte_dados)
                elif fonte_dados.endswith('.json'):
                    self.df = pd.read_json(fonte_dados)
            
            if self.df is not None:
                print(f"🚀 [LOAD] Dados carregados: {self.df.shape[0]} linhas x {self.df.shape[1]} colunas.")
            else:
                raise ValueError("Formato de arquivo não suportado.")
                
        except Exception as e:
            print(f"❌ [ERRO] Falha ao carregar: {str(e)}")

    def ver(self, linhas=5, titulo=None):
        """Mostra as primeiras linhas do dataset com um título opcional."""
        if self.df is not None:
            header = titulo if titulo else f"Primeiras {linhas} linhas"
            print(f"\n👀 [VIEW] {header}:")
            print(self.df.head(linhas))
        return self

    def sanitizar_colunas(self):
        """Padroniza nomes de colunas (snake_case) usando List Comprehension."""
        if self.df is not None:
            old_cols = self.df.columns
            new_cols = [
                col.strip().lower().replace(" ", "_").replace("/", "_").replace("-", "_") 
                for col in old_cols
            ]
            rename_map = {old: new for old, new in zip(old_cols, new_cols)}
            self.df.rename(columns=rename_map, inplace=True)
            print("✨ [CLEAN] Nomes das colunas padronizados.")
        return self

    def limpar_texto(self, colunas):
        """Aplica Title Case e remove espaços em colunas de texto."""
        if isinstance(colunas, str): colunas = [colunas]
        for col in colunas:
            if col in self.df.columns:
                self.df[col] = [
                    str(x).strip().title() if pd.notnull(x) else x 
                    for x in self.df[col]
                ]
                print(f"✨ [CLEAN] Texto da coluna '{col}' normalizado.")
        return self

    def remover_nulos(self, estrategia="apagar", preencher_com=0):
        """Trata valores ausentes."""
        antes = len(self.df)
        if estrategia == "apagar":
            self.df.dropna(inplace=True)
            print(f"🗑️ [DROP] {antes - len(self.df)} linhas com nulos removidas.")
        elif estrategia == "preencher":
            self.df.fillna(preencher_com, inplace=True)
            print(f"fill [FILL] Nulos preenchidos com '{preencher_com}'.")
        return self

    def converter_data(self, colunas, formato=None):
        """Converte colunas para datetime."""
        if isinstance(colunas, str): colunas = [colunas]
        for col in colunas:
            self.df[col] = pd.to_datetime(self.df[col], format=formato, errors='coerce')
            print(f"📅 [DATE] Coluna '{col}' convertida para data.")
        return self

    def criar_coluna(self, nome_nova_col, expressao_ou_func):
        """Cria coluna nova via string (eval) ou lambda."""
        try:
            if callable(expressao_ou_func):
                self.df[nome_nova_col] = self.df.apply(expressao_ou_func, axis=1)
            elif isinstance(expressao_ou_func, str):
                self.df.eval(f"{nome_nova_col} = {expressao_ou_func}", inplace=True)
            print(f"➕ [ADD] Coluna '{nome_nova_col}' criada.")
        except Exception as e:
            print(f"❌ [ERRO] Falha ao criar coluna: {e}")
        return self

    def filtrar(self, query_string):
        """Filtra dados (Ex: 'idade > 18')."""
        try:
            antes = len(self.df)
            self.df = self.df.query(query_string)
            print(f"🔍 [FILTER] '{query_string}': {antes} -> {len(self.df)} linhas.")
        except Exception as e:
            print(f"❌ [ERRO] Query inválida: {e}")
        return self

    def ordenar(self, colunas, ascendente=True):
        """Ordena o DataFrame."""
        self.df.sort_values(by=colunas, ascending=ascendente, inplace=True)
        print(f"sort [SORT] Ordenado por {colunas}.")
        return self

    def unir(self, outro_df, chaves, como="inner"):
        """Faz JOIN com outra tabela (DataFlow ou DataFrame)."""
        tabela_direita = outro_df.df if isinstance(outro_df, DataFlow) else outro_df
        antes = len(self.df)
        self.df = pd.merge(self.df, tabela_direita, on=chaves, how=como)
        print(f"🔗 [JOIN] Tabelas unidas ({como}). Linhas: {antes} -> {len(self.df)}")
        return self

    def plotar(self, tipo="barras", x=None, y=None, hue=None, titulo=None):
        """Gera gráficos com Seaborn."""
        plt.figure(figsize=(10, 6))
        sns.set_theme(style="whitegrid")
        try:
            if tipo == "barras":
                sns.barplot(data=self.df, x=x, y=y, hue=hue, palette="viridis")
            elif tipo == "linha":
                sns.lineplot(data=self.df, x=x, y=y, hue=hue)
            elif tipo == "scatter":
                sns.scatterplot(data=self.df, x=x, y=y, hue=hue, alpha=0.7)
            elif tipo == "hist":
                sns.histplot(data=self.df, x=x, kde=True, hue=hue)
            elif tipo == "box":
                sns.boxplot(data=self.df, x=x, y=y, hue=hue)
            
            plt.title(titulo if titulo else f"Gráfico de {tipo.title()}")
            plt.xlabel(x)
            plt.ylabel(y)
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.show()
        except Exception as e:
            print(f"❌ [ERRO] Falha ao plotar: {e}")
        return self

    def resumo_estatistico(self):
        """Mostra describe e dtypes."""
        print("\n📊 [STATS] Resumo Estatístico:")
        print(self.df.describe().T)
        print("\n📋 [TYPES] Tipos de Dados:")
        print(self.df.dtypes)
        return self

    def salvar(self, caminho):
        """Exporta o resultado."""
        try:
            if caminho.endswith('.csv'):
                self.df.to_csv(caminho, index=False)
            elif caminho.endswith('.xlsx'):
                self.df.to_excel(caminho, index=False)
            elif caminho.endswith('.parquet'):
                self.df.to_parquet(caminho)
            print(f"💾 [SAVE] Arquivo salvo em: {caminho}")
        except Exception as e:
            print(f"❌ [ERRO] Falha ao salvar: {e}")
        return self

    def pegar_dataframe(self):
        """Retorna o objeto pandas puro."""
        return self.df

    def auto_ml(self, alvo, tipo="classificacao", teste_tam=0.2, salvar_modelo=None):
        """
        Treina modelo automaticamente e salva com metadados de colunas.
        """
        from sklearn.model_selection import train_test_split
        from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
        from sklearn.metrics import accuracy_score, r2_score
        
        print(f"\n🤖 [AUTO-ML] Iniciando treinamento para prever: '{alvo}'...")

        try:
            # 1. Preparação Básica
            df_ml = self.df.dropna()
            X = df_ml.drop(columns=[alvo])
            y = df_ml[alvo]
            
            # Remove datas cruas
            cols_datas = X.select_dtypes(include=['datetime', 'datetimetz']).columns
            if len(cols_datas) > 0:
                print(f"   ⚠️ [INFO] Ignorando colunas de data crua para o modelo: {list(cols_datas)}")
                X = X.drop(columns=cols_datas)

            # 2. Encoding (Texto -> Número)
            X = pd.get_dummies(X, drop_first=True)
            print(f"   - Features processadas: {X.shape[1]} colunas (após encoding).")
            
            # 3. Split
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=teste_tam, random_state=42)
            
            # 4. Treino
            if tipo == "classificacao":
                modelo = RandomForestClassifier(n_estimators=100, random_state=42)
                modelo.fit(X_train, y_train)
                preds = modelo.predict(X_test)
                acc = accuracy_score(y_test, preds)
                print(f"   ✅ Modelo Classificador treinado!")
                print(f"   🎯 Acurácia: {acc:.2%}")
            else: # regressao
                modelo = RandomForestRegressor(n_estimators=100, random_state=42)
                modelo.fit(X_train, y_train)
                preds = modelo.predict(X_test)
                r2 = r2_score(y_test, preds)
                print(f"   ✅ Modelo Regressor treinado!")
                print(f"   🎯 R² Score: {r2:.4f}")

            # 5. Salvar (Blindado com colunas)
            if salvar_modelo:
                dados_ia = {
                    "modelo": modelo,
                    "colunas_treino": X.columns.tolist() # Salva a ordem exata das colunas
                }
                joblib.dump(dados_ia, salvar_modelo)
                print(f"   💾 Modelo blindado salvo em: {salvar_modelo}")
                
        except Exception as e:
            print(f"❌ [ERRO] Falha no Auto-ML: {e}")
            import traceback
            traceback.print_exc()
            
        return self

    def carregar_ia(self, caminho_modelo):
        """Carrega uma IA treinada pelo ds_flow."""
        try:
            dados_ia = joblib.load(caminho_modelo)
            self.modelo_ativo = dados_ia["modelo"]
            self.colunas_treino = dados_ia["colunas_treino"]
            print(f"🤖 [IA] Modelo carregado! Espera {len(self.colunas_treino)} colunas.")
        except Exception as e:
            print(f"❌ [ERRO] Falha ao carregar modelo: {e}")
        return self

    def prever(self, nome_coluna_saida="previsao"):
        """
        Usa a IA carregada para prever os dados atuais.
        Alinha as colunas automaticamente para evitar erros de produção.
        """
        if not hasattr(self, 'modelo_ativo'):
            raise ValueError("Você precisa usar .carregar_ia() antes de prever!")

        try:
            # 1. Prepara os dados atuais (Encoding)
            # Remove o alvo se ele existir por acaso nos dados novos (para não vazar resposta)
            # Mas aqui assumimos que df tem apenas as features
            
            # Remove datas cruas também na previsão para alinhar com o treino
            df_temp = self.df.copy()
            cols_datas = df_temp.select_dtypes(include=['datetime', 'datetimetz']).columns
            if len(cols_datas) > 0:
                df_temp = df_temp.drop(columns=cols_datas)

            df_pronto = pd.get_dummies(df_temp, drop_first=True)

            # 2. ALINHAMENTO DE COLUNAS (A Mágica da Produção)
            # Garante que todas as colunas do treino existam aqui (preenche com 0 se faltar)
            # E remove colunas extras que não existiam no treino
            df_pronto = df_pronto.reindex(columns=self.colunas_treino, fill_value=0)

            # 3. Previsão
            preds = self.modelo_ativo.predict(df_pronto)
            self.df[nome_coluna_saida] = preds
            
            print(f"🔮 [PREDICT] Previsões geradas na coluna '{nome_coluna_saida}'.")
        except Exception as e:
            print(f"❌ [ERRO] Falha na previsão: {e}")
            import traceback
            traceback.print_exc()
            
        return self