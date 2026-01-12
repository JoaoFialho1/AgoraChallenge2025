from src.models import APT
import pandas as pd

# Carregar results
df_retorno = pd.read_excel("projections/PROJECTIONS.xlsx", sheet_name='retornos', index_col=0)
df_fatores = pd.read_excel("projections/PROJECTIONS.xlsx", sheet_name='fatores', index_col=0)

df = df_retorno.join(df_fatores)

tickers = df_retorno.columns.tolist()
fatores = df_fatores.columns.tolist()


with pd.ExcelWriter('projections/APT.xlsx', engine='xlsxwriter') as writer:

    for ticker in tickers:
        resultados = APT(df, ticker, fatores, limite=3)
        resultados.to_excel(writer, sheet_name=ticker, index=False)