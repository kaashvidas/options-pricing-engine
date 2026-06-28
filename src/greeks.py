import numpy as np
from scipy.stats import norm
import matplotlib.pyplot as plt 
from black_scholes import black_scholes 

def compute_greeks(S, K, T, r, sigma, option_type='call'):
    """
    Compute analytical option Greeks from Black-Scholes formula.

    Delta: dC/dS- sensitivity of price to stock price move 
    Gamma: d^2C/dS^2- rate of change of Delta 
    Vega: dC/d(SIGMA) - sensitivity to volatility (per 1% move)
    Theta: dC/dT- time decay per calendar day (negative for long options)

    """
    # Get d1 and d2 from our BS function 
    _, d1, d2= black_scholes(S, K, T, r, sigma, option_type)
    
    # Delta: N(d1) for call, N(d1)-1 for put 
    if option_type=='call':
        delta= norm.cdf(d1)
    else:
        delta= norm.cdf(d1)-1
    
    #Gamma: same for calls and puts 
    gamma= norm.pdf(d1)/ (S* sigma* np.sqrt(T))

    #Vega: expressed per 1% change in volatility
    vega= S* norm.pdf(d1)*np.sqrt(T)/100

    #Theta: time decay per calendar day
    term1= -(S* norm.pdf(d1)*sigma)/(2* np.sqrt(T))
    if option_type=='call':
        theta= (term1- r*K* np.exp(-r*T)* norm.cdf(d2))/365
    else: 
        theta= (term1+r* K* np.exp(-r*T)* norm.cdf(-d2))/365

    return{
        'delta': delta,
        'gamma': gamma, 
        'vega': vega, 
        'theta': theta
    }

def plot_delta_curve(K, T, r, sigma, save_path= 'delta_curve.png'):
    """
    Plot Delta vs Stock Price for a call option.
    Should form an S-curve from 0 (deep OTM) TO 1 (deep ITM).
    This is one of the most intuitive visualisations in options theory.
    """
    stock_prices= np.linspace(50, 150, 300)
    deltas= [compute_greeks(S, K, T, r, sigma, 'call')['delta'] for S in stock_prices]

    plt.figure(figsize=(9,5))
    plt.plot(stock_prices, deltas, color= 'steelblue', linewidth=2.5)
    plt.axvline(x=K, color='orange', linestyle= '--', linewidth=1.5, label= f'Strike price K= {K}')
    plt.axhline(y=0.5, color='gray', linestyle=':', linewidth=1, label= 'Delta= 0.5(at-the-money)')
    plt.xlabel('Stock Price S', fontsize=12)
    plt.ylabel('Delta', fontsize=12)
    plt.title('Call Option Delta vs Stock Price\n' '(S-curve: Delta-> 0 deep OTM, Delta-> 1 deep ITM)', fontsize=12)
    plt.legend(fontsize=10)
    plt.ylim(-0.05, 1.05)
    plt.grid(True, alpha= 0.3)
    plt.tight_layout()
    plt.savefig(save_path, dpi=150)
    plt.show()
    print(f"Plot saved to {save_path}")

if __name__=='__main__':
    S, K, T, r, sigma= 100, 100, 1, 0.05, 0.2 
    greeks= compute_greeks(S, K, T, r, sigma, 'call')

    print("Option Greeks (Call, S=K=100, T=1yr, r=5%, sigma=20%)")

    print("-"* 45)

    for name, value, in greeks.items():
        print(f"{name.capitalize():8s}: {value:+.6f}")

    # Sanity checks 
    print("\n Sanity Checks: ")
    print(f"Delta should be between 0 and 1 for a call: {0 < greeks['delta'] < 1}")
    print(f"Gamma should be positive: {greeks['gamma'] > 0}")
    print(f"Vega should be positive: {greeks['vega'] > 0}")
    print(f"Theta should be negative (time decay): {greeks['theta'] < 0}")
  
    plot_delta_curve(K, T, r, sigma)