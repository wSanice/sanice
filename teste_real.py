import pandas as pd
from ds_flow import DataFlow

print("--- 1. FASE DE TREINAMENTO (Gerando o arquivo correto) ---")

dados_treino = {
    'Data Venda': ['2023-01-15', '2023-01-18', '2023-02-01', '2023-02-10', '2023-03-05', None],
    'Produto': ['Notebook Gamer', 'Mouse Sem Fio', 'Notebook Gamer', 'Teclado Mecânico', 'Mouse Sem Fio', 'Cabo HDMI'],
    'Valor': [4500.00, 150.50, 4200.00, 350.00, 120.00, 50.00],
    'Cliente VIP': ['Sim', 'Não', 'Sim', 'Não', 'Sim', 'Não']
}
df_treino = pd.DataFrame(dados_treino)

(DataFlow(df_treino)
    .sanitizar_colunas()
    .remover_nulos()
    .auto_ml(alvo="cliente_vip", salvar_modelo="modelo_vip.pkl")
)

print("\n--- 2. FASE DE PRODUÇÃO (Testando o arquivo novo) ---")
dados_novos = {
    'Produto': ['Notebook Gamer', 'Mouse Sem Fio'], 
    'Valor': [4600.00, 140.00]
}
df_hoje = pd.DataFrame(dados_novos)

(DataFlow(df_hoje)
    .ver(titulo="Dados Novos")
    .carregar_ia("modelo_vip.pkl")
    .prever(nome_coluna_saida="previsao_vip")
    .ver(titulo="Resultado Final")
)
