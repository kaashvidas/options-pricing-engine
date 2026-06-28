import numpy as np 
from scipy.stats import norm

def black_scholes(S, K, T, r, sigma, option_type= 'call'):
    """
    Compute European option price using the Black-Scholes formula.

    Parameters 
    -----------
    S: float Current Stock Price 
    K: float Strike Price 
    T: float Time to expiry in years (e.g. 0.5+ 6 months)
    r: float Risk-free interest rate (annualised, e.g. 0.05= 5%)
    sigma: float Volatility of the stock (annualised, e.g. 0.2= 20%)
    optons_type: str 'call' or 'put' 

    Returns 
    -------
    price: float Option price 
    d1: float Intermediate value (used by Greeks)
    d2: float intermediate value (used by Greeks)

    """
    # d1 and d2 are intermediate standardised values 
    d1= (np.log(S/K)+ (r+ 0.5* sigma**2)* T)/(sigma* np.sqrt(T))
    d2= d1- sigma* np.sqrt(T)

    if option_type== 'call':
        # Call: right to BUY at strike K
        price= S* norm.cdf(d1)- K*np.exp(-r* T) * norm.cdf(d2)
    elif option_type== 'put':
        # Put: right to SELL at strike price K
        price= K* np.exp(-r* T)* norm.cdf(-d2)-S * norm.cdf(-d1)
    else: 
        raise ValueError("option_type must be 'call' or 'put' ")

    return price, d1, d2

if __name__=='__main__':
    S, K, T, r, sigma= 100, 100, 1, 0.05, 0.2

    call_price, d1, d2= black_scholes(S, K, T, r, sigma, 'call')
    put_price, _, _= black_scholes(S, K, T, r, sigma, 'put')

    print (f"Call Price : {call_price:.4f}")
    print (f"Put price : {put_price:.4f}")
    print (f"d1={d1:.4f} d2={d2:.4f}")

    # Verify put-call parity: C-P should equal S- K* e^(-rT)
    parity_lhs= call_price- put_price 
    parity_rhs= S- K * np.exp(-r*T)
    print (f"Put-call parity check: {parity_lhs: .4f} vs {parity_rhs:.4f}")
    print("Parity holds:", abs(parity_lhs- parity_rhs)<0.001)
