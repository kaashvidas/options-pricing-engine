# Options Pricing Engine & Volatility Surface Analysis

## Overview

An implementation of European option pricing using three approaches:
Black-Scholes closed-form solution, Monte Carlo simulation, and analytical
Greeks. Built to connect theoretical probability and stochastic calculus
concepts to real financial markets.

## What This Project Covers

- **Black-Scholes pricing** — closed-form formula for European call and put options
- **Monte Carlo simulation** — GBM-based path simulation with convergence analysis
- **Option Greeks** — Delta, Gamma, Vega, Theta computed analytically
- **Visualisations** — convergence plot, Delta sensitivity curve

## Mathematical Background

The Black-Scholes formula assumes stock prices follow Geometric Brownian Motion:

```
dS = μS dt + σS dW
```

Under risk-neutral measure, the European call price is:

```
C = S·N(d₁) - K·e^(-rT)·N(d₂)

where:
  d₁ = [ln(S/K) + (r + σ²/2)T] / (σ√T)
  d₂ = d₁ - σ√T
  N(·) = cumulative standard normal distribution
```

Monte Carlo simulation approximates this by simulating N paths of the terminal
stock price S_T = S·exp((r - 0.5σ²)T + σ√T·Z), where Z ~ N(0,1), computing
the payoff for each path, and discounting the average back to present value.

## Results

**Test case:** S=100, K=100, T=1yr, r=5%, σ=20%

| Method | Call Price |
|--------|-----------|
| Black-Scholes (analytical) | 10.4506 |
| Monte Carlo (1,000,000 paths) | ~10.45 ± 0.02 |

**Greeks at this parameter set:**

| Greek | Value | Interpretation |
|-------|-------|----------------|
| Delta | +0.6368 | Option price increases $0.64 per $1 rise in stock |
| Gamma | +0.0188 | Delta changes by 0.019 per $1 stock move |
| Vega  | +0.3753 | Price increases $0.38 per 1% rise in volatility |
| Theta | -0.0142 | Option loses $0.014 in value per calendar day |

## Visualisations

### Monte Carlo Convergence
![Monte Carlo Convergence](convergence_plot.png)

*As simulation count increases (x-axis, log scale), the MC estimate (blue)
converges to the Black-Scholes analytical price (orange dashed). This
demonstrates the Law of Large Numbers numerically.*

### Delta Sensitivity Curve
![Delta Curve](delta_curve.png)

*Delta forms an S-curve from ~0 (deep out-of-the-money) to ~1 (deep
in-the-money). At S=K=100 (at-the-money), Delta ≈ 0.5. This means a
market maker holding one call option can hedge by shorting 0.64 shares.*

## Project Structure

```
options-pricing-engine/
├── black_scholes.py    # BS formula — price, d1, d2
├── monte_carlo.py      # GBM simulation + convergence plot
├── greeks.py           # Delta, Gamma, Vega, Theta + Delta curve
├── main.py             # runs full pipeline
└── requirements.txt
```

## How to Run

```bash
pip install -r requirements.txt
python black_scholes.py    # verify BS formula
python monte_carlo.py      # run simulation + generate convergence plot
python greeks.py           # compute Greeks + generate Delta curve
python main.py             # run complete pipeline
```

## Coursework

This project directly applies concepts from:
- **Probability & Stochastic Processes** — Geometric Brownian Motion, risk-neutral
  pricing, Monte Carlo methods
- **Computational Linear Algebra** — matrix operations in vectorised NumPy simulation
- **Real Analysis** — convergence of MC estimator (Law of Large Numbers in practice)


