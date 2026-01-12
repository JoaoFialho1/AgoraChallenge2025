import pandas as pd
from itertools import combinations
import statsmodels.api as sm

def CAPM(df, ticker, year, rf=0.02, market='Índice Bolsa'):

    # FILTER DATA BY YEARS
    df = df[df['Ano'] == year]

    # BETA
    cov = df[ticker].cov(df[market])
    var_m = df[market].var()
    beta = cov / var_m

    # MARKET RETURN MEAN
    market_mean = df[market].mean()

    # EXPECTED RETURN
    expected_return = rf + beta * (market_mean - rf)

    # OUTPUT
    output = pd.DataFrame({'Ano': [year], 'Beta': [beta], 'Retorno_Esperado': [expected_return]})
    return output


def APT(df, y_col, fatores, alfa=0.04, limite=5):
    resultados = []

    # Gera todas as combinações de até 5 fatores
    for k in range(1, min(len(fatores), limite) + 1):
        for subset in combinations(fatores, k):
            X = df[list(subset)]
            X = sm.add_constant(X)
            Y = df[y_col]

            modelo = sm.OLS(Y, X).fit()

            # Evita casos sem graus de liberdade
            if modelo.df_resid == 0:
                continue

            linha = {'Fatores Usados': ', '.join(subset)}

            # Conta quantas variáveis individuais são significativas
            num_significativos = 0
            for f, coef in modelo.params.items():
                linha[f] = coef
                if f != 'const' and modelo.pvalues[f] < alfa:
                    num_significativos += 1

            linha['Var_signif'] = num_significativos
            linha['R2 Ajustado'] = modelo.rsquared_adj
            linha['SQR'] = sum(modelo.resid ** 2)
            linha['BIC'] = modelo.bic
            linha['pv(F)'] = modelo.f_pvalue

            resultados.append(linha)

    # Converte resultados em DataFrame
    df_resultados = pd.DataFrame(resultados)

    # Ordena colunas de forma lógica
    col_ordem = ['Fatores Usados', 'Var_signif', 'R2 Ajustado', 'SQR', 'BIC', 'pv(F)']
    if 'const' in df_resultados.columns:
        col_ordem.append('const')
    col_ordem += [c for c in df_resultados.columns if c not in col_ordem]

    df_resultados = df_resultados[col_ordem]

    return df_resultados