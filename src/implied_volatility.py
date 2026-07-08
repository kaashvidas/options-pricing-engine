
import numpy as np
import pandas as pd
import yfinance as yf
from scipy.optimize import brentq
import warnings
warnings.filterwarnings("ignore")

from black_scholes import black_scholes


def implied_volatility(market_price, S, K, T, r, option_type="call"):
    if T <= 0:
        return np.nan

    if option_type == "call":
        lower_bound = max(0, S - K * np.exp(-r * T))
    else:
        lower_bound = max(0, K * np.exp(-r * T) - S)

    if market_price <= lower_bound + 1e-8:
        return np.nan

    def objective(sigma):
        price, _, _ = black_scholes(S, K, T, r, sigma, option_type)
        return price - market_price

    try:
        return brentq(objective, 1e-3, 5.0, maxiter=200)
    except (ValueError, RuntimeError):
        return np.nan


def fetch_options_chain(ticker="SPY", r=0.05):
    stock = yf.Ticker(ticker)

    history = stock.history(period="1d")
    if history.empty:
        raise ValueError(f"Unable to fetch price data for {ticker}")

    S = history["Close"].iloc[-1]
    print(f"Current {ticker} price: ${S:.2f}")

    expiries = stock.options
    if not expiries:
        raise ValueError(f"No options available for {ticker}")

    print(f"Found {len(expiries)} expiry dates")

    today = pd.Timestamp.today().normalize()
    all_rows = []

    for expiry in expiries[:10]:
        chain = stock.option_chain(expiry)
        expiry_date = pd.Timestamp(expiry)
        T = (expiry_date - today).days / 365.0

        if T <= 0.01:
            continue

        for _, row in chain.calls.iterrows():

            market_price = row["lastPrice"]

            if pd.isna(market_price) or market_price <= 0:
                bid = row["bid"] if not pd.isna(row["bid"]) else 0
                ask = row["ask"] if not pd.isna(row["ask"]) else 0
                market_price = (bid + ask) / 2

            if pd.isna(market_price) or market_price <= 0.05:
                continue

            moneyness = row["strike"] / S
            if moneyness < 0.85 or moneyness > 1.15:
                continue

            iv = implied_volatility(
                market_price,
                S,
                row["strike"],
                T,
                r,
                "call",
            )

            all_rows.append({
                "strike": row["strike"],
                "expiry": expiry,
                "T": T,
                "market_price": market_price,
                "iv": iv,
                "option_type": "call",
                "bid": row["bid"],
                "ask": row["ask"],
                "moneyness": moneyness,
            })

    df = pd.DataFrame(all_rows)

    if df.empty:
        print("No option data collected.")
        return df, S

    df = df.dropna(subset=["iv"])
    df = df[(df["iv"] > 0.01) & (df["iv"] < 3.0)]
    df = df.sort_values(["expiry", "strike"]).reset_index(drop=True)

    print(f"Computed IV for {len(df)} options across {df['expiry'].nunique()} expiries")
    return df, S


if __name__ == "__main__":
    df, S = fetch_options_chain("SPY")

    print("\nSample IV Results:\n")
    print(df[["strike", "expiry", "T", "market_price", "iv"]].head(10).to_string(index=False))

    if not df.empty:
        print(f"\nIV Range : {df['iv'].min():.2%} - {df['iv'].max():.2%}")
        print(f"Median IV: {df['iv'].median():.2%}")
