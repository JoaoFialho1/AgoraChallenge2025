from src.markowitz import markowitz_monte_carlo
import pandas as pd

#=================INPUTS===============#
expected_returns = pd.read_excel('results/expected_return_4y.xlsx', sheet_name='6modelo', index_col=0)

prices = pd.read_excel('results/PROJECTIONS.xlsx', sheet_name='precos')
prices = prices[expected_returns.index]
returns = prices.pct_change()


#=============MARKOWITZ============#
markowitz_monte_carlo(name='6ano_4_APT', returns=returns, expected_returns=expected_returns,
                      risk_free=0.02, n_portfolios=1000000)