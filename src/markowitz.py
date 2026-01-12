import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def markowitz_monte_carlo(name, returns, expected_returns, risk_free=0.02, n_portfolios=100000):

    # Parameters
    cov_matrix = returns.cov() * 252
    num_assets = len(expected_returns)

    # Covert to array
    expected_returns = expected_returns.values.flatten()

    #==============GENERATE-RANDOM-PORTFOLIOS================#

    # Portfolios
    portfolios_dict = {"Sharpe": [], "Return": [], "Volatility": []}
    portfolios_dict.update({asset: [] for asset in returns.columns})

    for portfolio in range(n_portfolios):
        # Random weight
        weights_raw = np.zeros(num_assets)
        for i in range(num_assets):
            if expected_returns[i] >= 0:
                # retorno esperado positivo → peso normal aleatório
                weights_raw[i] = np.random.randint(0, 1001) / 1000
            else:
                # retorno esperado negativo → peso pequeno e aleatório entre 0% e 5%
                weights_raw[i] = np.random.randint(0, 51) / 1000


        # Add signal to short or long
        weights_signed  = weights_raw * np.sign(expected_returns)

        # Normalize
        weights = weights_signed / np.sum(np.abs(weights_signed))

        # Results
        portfolio_returns = weights.T @ expected_returns
        portfolio_volatility = np.sqrt(weights.T @ cov_matrix.values @ weights)

        # Sharpe
        if portfolio_volatility==0:
            sharpe = np.nan
        else:
            sharpe = (portfolio_returns - risk_free) / portfolio_volatility


    # ===================EXPORT-DATAS========================#

        # Export datas
        for i, ticker in enumerate(returns.columns):
            portfolios_dict[ticker].append(weights[i])
        portfolios_dict["Sharpe"].append(sharpe)
        portfolios_dict["Return"].append(portfolio_returns)
        portfolios_dict["Volatility"].append(portfolio_volatility)

    portfolios_dict = pd.DataFrame(portfolios_dict)


    # ===============SAVE-PORTFOLIOS==================#

    # Save inputs
    portfolios_dict.to_excel(f'dados/{name}_portfolios_markowitz.xlsx')


    #===============PLOT-EFFICIENT-FRONTIER==================#

    # Portfolio with best Sharpe
    idx_max_sharpe = portfolios_dict['Sharpe'].idxmax()
    best_portfolio = portfolios_dict.loc[idx_max_sharpe]

    # Plot Returns x Volatility rainbow by Sharpe
    fig, ax = plt.subplots(figsize=(12, 8))
    scatter = ax.scatter(
        portfolios_dict['Volatility'],
        portfolios_dict['Return'],
        c=portfolios_dict['Sharpe'],
        cmap='viridis',
        alpha=0.6)

    # Best Sharpe
    ax.scatter(
        best_portfolio['Volatility'],
        best_portfolio['Return'],
        color='red',
        marker='*',
        s=300,  # Star size
        label='Best Sharpe')

    # Parameters of graph
    ax.set_xlabel('Volatility')
    ax.set_ylabel('Expected return')
    ax.set_title(f'Efficient frontier (Monte Carlo)')
    ax.grid(True)

    # Sharpe colorbar
    cbar = fig.colorbar(scatter, ax=ax)
    cbar.set_label('Sharpe Ratio')

    # Save Plot
    fig.savefig(f'dados/{name}_efficient_frontier.png', dpi=300)
    plt.show()