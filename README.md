# Options Pricing Engine & Volatility Surface Analysis

## Overview

A quantitative finance project implementing European option pricing using multiple numerical and analytical methods. The project includes Black-Scholes pricing, Monte Carlo simulation, implied volatility estimation, analytical Greeks, interactive visualisations, and a Streamlit web application for real-time option analysis.

**Live Demo:** https://options-pricing-engine-kaashvi.streamlit.app/

---

## Features

- **Black-Scholes Pricing** — Closed-form pricing for European call and put options
- **Monte Carlo Simulation** — Geometric Brownian Motion (GBM) based simulation with convergence analysis
- **Implied Volatility Solver** — Newton-Raphson method to estimate market-implied volatility
- **Option Greeks** — Analytical computation of Delta, Gamma, Vega, Theta, and Rho
- **Interactive Streamlit Dashboard** — Real-time pricing with user-defined market parameters
- **Visualisations**
  - Monte Carlo convergence
  - Delta sensitivity curve

---

## Mathematical Background

### Geometric Brownian Motion

The Black-Scholes model assumes that stock prices follow Geometric Brownian Motion:

```
dS = μS dt + σS dW
```

where

- **S** = stock price
- **μ** = expected return
- **σ** = volatility
- **dW** = Brownian motion

---

### Black-Scholes Formula

The European call option price is given by

```
C = S·N(d₁) − K·e^(−rT)·N(d₂)
```

where

```
d₁ = [ln(S/K) + (r + σ²/2)T] / (σ√T)

d₂ = d₁ − σ√T
```

and **N(·)** denotes the cumulative standard normal distribution.

---

### Monte Carlo Pricing

Monte Carlo simulation estimates the option price by simulating a large number of terminal stock prices:

```
S_T = S · exp((r − 0.5σ²)T + σ√T Z)
```

where

```
Z ~ N(0,1)
```

The discounted average payoff converges to the Black-Scholes price as the number of simulations increases.

---

## Implied Volatility

The project estimates implied volatility from market prices using the **Newton-Raphson iterative method**.

Given a market option price, the algorithm repeatedly updates volatility until the theoretical Black-Scholes price matches the observed market price.

---

## Results

### Sample Parameters

| Parameter | Value |
|-----------|------:|
| Stock Price (S) | 100 |
| Strike Price (K) | 100 |
| Time to Expiry (T) | 1 year |
| Risk-free Rate (r) | 5% |
| Volatility (σ) | 20% |

### Pricing Comparison

| Method | Call Price |
|---------|-----------:|
| Black-Scholes | 10.4506 |
| Monte Carlo (1,000,000 paths) | ~10.45 ± 0.02 |

### Greeks

| Greek | Value | Interpretation |
|--------|------:|---------------|
| Delta | +0.6368 | Price sensitivity to stock price |
| Gamma | +0.0188 | Rate of change of Delta |
| Vega | +0.3753 | Sensitivity to volatility |
| Theta | -0.0142 | Time decay |
| Rho | +0.5323 | Sensitivity to interest rates |

---

## Visualisations

### Monte Carlo Convergence

![Monte Carlo Convergence](convergence_plot.png)

As the number of simulated paths increases, the Monte Carlo estimate converges toward the analytical Black-Scholes price, illustrating the **Law of Large Numbers**.

---

### Delta Sensitivity Curve

![Delta Curve](delta_curve.png)

The Delta curve transitions smoothly from approximately **0** (deep out-of-the-money) to **1** (deep in-the-money), showing how option sensitivity changes with the underlying asset price.

---

## Streamlit Web Application

The project is deployed as an interactive Streamlit application where users can:

- Input custom market parameters
- Price European call and put options instantly
- Compare Black-Scholes and Monte Carlo results
- Calculate implied volatility from market prices
- View option Greeks
- Experiment with different market scenarios interactively

**Live Demo:** https://options-pricing-engine-kaashvi.streamlit.app/

---

## Project Structure

```
options-pricing-engine/
│
├── black_scholes.py
├── monte_carlo.py
├── greeks.py
├── implied_volatility.py
├── app.py                 # Streamlit application
├── main.py
├── requirements.txt
├── convergence_plot.png
├── delta_curve.png
└── README.md
```

---

## Installation

Clone the repository

```bash
git clone <repository-url>
cd options-pricing-engine
```

Install dependencies

```bash
pip install -r requirements.txt
```

---

## Running the Project

Run individual modules

```bash
python black_scholes.py
python monte_carlo.py
python greeks.py
python implied_volatility.py
```

Run the complete pipeline

```bash
python main.py
```

Launch the Streamlit app locally

```bash
streamlit run app.py
```

---

## Coursework Connections

This project applies concepts from

- **Probability & Stochastic Processes**
  - Geometric Brownian Motion
  - Risk-neutral pricing
  - Monte Carlo methods

- **Real Analysis**
  - Numerical convergence
  - Law of Large Numbers

- **Computational Mathematics**
  - Vectorised NumPy implementation
  - Numerical root-finding using Newton-Raphson

- **Quantitative Finance**
  - Black-Scholes model
  - Option Greeks
  - Implied volatility estimation
  - Derivatives pricing

---

## Tech Stack

- Python
- NumPy
- SciPy
- Matplotlib
- Streamlit

---

## Future Improvements

- Historical volatility estimation from real market data
- Volatility smile and volatility surface visualisation
- Binomial and Trinomial pricing models
- American option pricing
- Barrier and Asian option pricing
- Live market data integration using financial APIs