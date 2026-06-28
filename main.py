from black_scholes import black_scholes 
from monte_carlo import monte_carlo_option, plot_convergence 
from greeks import compute_greeks, plot_delta_curve 

S, K, T, r, sigma= 100, 100, 1, 0.05, 0.2

print('='* 50)
print ("OPTIONS PRICING ENGINE")
print('='*50)

#Black-Scholes 
call, _, _= black_scholes(S, K, T, r, sigma, 'call')
put, _, _= black-scholes(S, K, T, r, sigma, 'put')
print(f"\n[Black-Scholes] Call= {call:.4f} Put= {put:.4f}")

#Monte-Carlo
mc_price, mc_se= monte_carlo_option(S, K, T, r, sigma, n_simulations=500_000)
print(f"[Monte Carlo] Call= {mc_price:.4f}+- {mc.se:.4f}")

#Greeks 
g= compute_greeks(S, K, T, r, sigma, 'call')
print(f"\n[Greeks]")
for name, val in g.items():
    print(f"{name.capitalize():8s}: {val:+.6f}")

# Generate plots 
print("\n Generating plots...")
plot_convergence(S, K, T, r, sigma)
plot_delta_curve(K, T, r, sigma)
print("Done. Plots saved.")
