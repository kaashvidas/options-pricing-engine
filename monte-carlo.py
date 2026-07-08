import numpy as np 
import matplotlib.pyplot as plt 
from black_scholes import black_scholes 

def monte_carlo_options(S, K, T, r, sigma, option_type='call', n_simulations=100_000):
    """
    Price a European option using Monte Carlo simulation.

    Simulates n_simulations path of the stock price at expiry using Geometric Brownian Motion, computes payoff for each path, 
    and discounts the average patoff back to present value.

    """
    # Draw standard normal random variables- one per simulated path
    Z= np.random.standard_normal(n_simulations)

    # Simulate terminal stock price for each path (GBM, single step)
    S_T= S* np.exp((r-0.5* sigma**2)* T+ sigma* np.sqrt(T)*Z)

    #Compute option payoff at expiry for each simulated path 
    if option_type=='call':
        payoffs= np.maximum(S_T-K, 0)
    else: 
        payoffs= np.maximum(K-S_T, 0)

    # Discount average payoff back to today
    price= np.exp(-r*T)* np.mean(payoffs)

    #Standard error of the estimate (measures simulation uncertainty)
    std_error= np.exp(-r*T)* np.std(payoffs)/ np.sqrt(n_simulations)

    return price, std_error 

def plot_convergence(S, K, T, r, sigma, save_path='convergence_plot.png'):
    """
    Show how the Monte Carlo estimate converges to the Black-Scholes analytical price as the number of simulations increases. This 
    demonstrates the law of large numbers visually.
    """
    #True analytical price from the Black-Scholes 
    bs_price, _, _= black_scholes(S, K, T, r, sigma, 'call')

    # Range of simulation counts (log scale for visual clarity)
    sim_sizes= [100, 500, 1_000, 5_000, 10_000, 50_000, 100_000, 500_000]
    mc_prices=[]

    for n in sim_sizes:
        price, _= monte_carlo_options(S, K, T, r, sigma, n_simulations=n)
        mc_prices.append(price)

    #Plot 
    plt.figure(figsize=(10,5))
    plt.semilogx(sim_sizes, mc_prices, 'o-', color='steelblue', linewidth=2, label='Monte Carlo estimate')
    plt.axhline(y=bs_price, color= 'orange', linestyle='--', linewidth=2, label=f'Black-Scholes price: {bs_price:.4f}')
    plt.xlabel('Number of Simulations (log scale)', fontsize=12)
    plt.ylabel('Estimated Option Price', fontsize=12)
    plt.title('Monte Carlo Convergence to Black-Scholes Analytical Price', fontsize=13)
    plt.legend(fontsize=11)
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(save_path, dpi=150)
    plt.show()
    print(f"Plot saved to {save_path}")

if __name__=='__main__':
    S, K, T, r, sigma= 100, 100, 1, 0.05, 0.2

    #Single estimate with many simulations 
    price, se= monte_carlo_option(S, K, T, r, sigma, n_simulations=1_000_000)
    bs_price, _, _= black_scholes(S, K, T, r, sigma, 'call')

    print (f"Monte Carlo price: {price:.4f}+- {se:.4f}")
    print (f"Black-Scholes price: {bs_price:.4f}")
    price (f"Difference: {abs(price- bs_price):.4f}")

    # Generate convergence plot 
    plot_convergence(S, K, T, r, sigma)

