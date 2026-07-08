import streamlit as st
import numpy as np
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import pandas as pd

from black_scholes import black_scholes
from monte_carlo import monte_carlo_option
from greeks import compute_greeks

# --- Page config ---
st.set_page_config(
    page_title="Options Pricing Engine",
    page_icon="📈",
    layout="wide"
)

# --- Header ---
st.title("📈 Options Pricing Engine")
st.markdown(
    """
    **Black-Scholes · Monte Carlo · Greeks · Implied Volatility**
    
    Adjust inputs in the sidebar to see real-time option pricing and risk metrics.
    Built from scratch using the mathematical framework of Geometric Brownian Motion.
    """
)
st.divider()

# --- Sidebar inputs ---
st.sidebar.header("Option Parameters")

S = st.sidebar.slider(
    "Stock Price (S)", min_value=50.0, max_value=300.0,
    value=100.0, step=1.0,
    help="Current price of the underlying stock"
)
K = st.sidebar.slider(
    "Strike Price (K)", min_value=50.0, max_value=300.0,
    value=100.0, step=1.0,
    help="Price at which you can buy (call) or sell (put) the stock"
)
T = st.sidebar.slider(
    "Time to Expiry (years)", min_value=0.1, max_value=3.0,
    value=1.0, step=0.05,
    help="0.25 = 3 months, 0.5 = 6 months, 1.0 = 1 year"
)
r = st.sidebar.slider(
    "Risk-Free Rate", min_value=0.0, max_value=0.15,
    value=0.05, step=0.005,
    format="%.3f",
    help="Annualised risk-free interest rate (approx 10-yr government bond yield)"
)
sigma = st.sidebar.slider(
    "Volatility (σ)", min_value=0.05, max_value=1.0,
    value=0.20, step=0.01,
    format="%.2f",
    help="Annualised volatility. AAPL ≈ 0.25, S&P 500 ≈ 0.15"
)
option_type = st.sidebar.selectbox(
    "Option Type", ["call", "put"],
    help="Call = right to buy. Put = right to sell."
)
n_sims = st.sidebar.select_slider(
    "Monte Carlo Simulations",
    options=[1_000, 10_000, 50_000, 100_000],
    value=10_000,
    help="More simulations = more accurate but slower"
)

# --- Tabs ---
tab1, tab2, tab3 = st.tabs([
    "💰 Pricing & Greeks",
    "📊 Sensitivity Plots",
    "🌊 Volatility Surface"
])

# =================== TAB 1: PRICING & GREEKS ===================
with tab1:
    # Compute all values
    bs_price, d1, d2 = black_scholes(S, K, T, r, sigma, option_type)
    mc_price, mc_se  = monte_carlo_option(S, K, T, r, sigma, option_type, n_sims)
    greeks           = compute_greeks(S, K, T, r, sigma, option_type)

    # --- Price comparison ---
    st.subheader("Option Price")
    col1, col2, col3 = st.columns(3)
    col1.metric("Black-Scholes Price", f"${bs_price:.4f}")
    col2.metric("Monte Carlo Price",  f"${mc_price:.4f}",
                delta=f"±{mc_se:.4f} (std error)")
    col3.metric("MC vs BS Difference",
                f"${abs(mc_price - bs_price):.4f}",
                delta=f"{abs(mc_price-bs_price)/bs_price*100:.2f}%")

    st.divider()

    # --- Greeks ---
    st.subheader("Option Greeks")
    g1, g2, g3, g4 = st.columns(4)
    g1.metric("Delta (Δ)", f"{greeks['delta']:+.4f}",
              help="Price change per $1 move in stock")
    g2.metric("Gamma (Γ)", f"{greeks['gamma']:+.4f}",
              help="Rate of change of Delta")
    g3.metric("Vega  (ν)", f"{greeks['vega']:+.4f}",
              help="Price change per 1% move in volatility")
    g4.metric("Theta (Θ)", f"{greeks['theta']:+.4f}",
              help="Price lost per calendar day (time decay)")

    st.divider()

    # --- Intermediate values ---
    st.subheader("Intermediate Values")
    v1, v2, v3 = st.columns(3)
    v1.metric("d1", f"{d1:.4f}")
    v2.metric("d2", f"{d2:.4f}")
    v3.metric("Moneyness (S/K)", f"{S/K:.3f}",
              delta="ITM" if (option_type=='call' and S>K) else "OTM")

    # --- Explanation ---
    with st.expander("📖 What do these numbers mean?"):
        st.markdown(f"""
**Option Price ${bs_price:.2f}** — This is what the option contract should cost today
under the Black-Scholes model.

**Delta {greeks['delta']:+.3f}** — If AAPL moves up by $1, this option's value changes
by approximately ${greeks['delta']:+.3f}. A delta-neutral portfolio would short
{abs(greeks['delta']):.2f} shares for every option held.

**Theta {greeks['theta']:+.4f}** — This option loses ${abs(greeks['theta']):.4f} in
value every calendar day, assuming all else constant. Over a week: ${abs(greeks['theta'])*7:.3f}.

**Vega {greeks['vega']:+.4f}** — If implied volatility rises by 1%, this option gains
${greeks['vega']:+.4f} in value. High vega means the option is very sensitive to
market uncertainty.
        """)

# =================== TAB 2: SENSITIVITY PLOTS ===================
with tab2:
    st.subheader("Delta vs Stock Price")

    stock_prices = np.linspace(S * 0.5, S * 1.5, 300)
    deltas = [compute_greeks(sp, K, T, r, sigma, option_type)['delta']
              for sp in stock_prices]

    fig_delta = go.Figure()
    fig_delta.add_trace(go.Scatter(
        x=stock_prices, y=deltas, mode='lines',
        line=dict(color='steelblue', width=2.5),
        name='Delta'
    ))
    fig_delta.add_vline(
        x=K, line_dash='dash', line_color='orange',
        annotation_text=f"Strike K={K}"
    )
    fig_delta.add_vline(
        x=S, line_dash='dot', line_color='red',
        annotation_text=f"Current S={S}"
    )
    fig_delta.update_layout(
        title="Delta S-Curve — How Delta Changes With Stock Price",
        xaxis_title="Stock Price",
        yaxis_title="Delta",
        height=400
    )
    st.plotly_chart(fig_delta, use_container_width=True)

    st.subheader("Option Price vs Volatility")
    sigmas = np.linspace(0.05, 0.8, 100)
    prices = [black_scholes(S, K, T, r, sig, option_type)[0] for sig in sigmas]

    fig_vega = go.Figure()
    fig_vega.add_trace(go.Scatter(
        x=sigmas * 100, y=prices, mode='lines',
        line=dict(color='mediumpurple', width=2.5),
        name='Option Price'
    ))
    fig_vega.add_vline(
        x=sigma * 100, line_dash='dash', line_color='orange',
        annotation_text=f"Current σ={sigma:.0%}"
    )
    fig_vega.update_layout(
        title="Option Price vs Volatility — Vega Relationship",
        xaxis_title="Volatility (%)",
        yaxis_title="Option Price",
        height=400
    )
    st.plotly_chart(fig_vega, use_container_width=True)

# =================== TAB 3: VOLATILITY SURFACE ===================
with tab3:
    st.subheader("Live AAPL Implied Volatility Surface")
    st.info("Fetching live options data from Yahoo Finance. This may take 15–30 seconds.")

    @st.cache_data(ttl=3600)   # cache for 1 hour — avoid re-fetching on every slider move
    def load_iv_data():
        from implied_volatility import fetch_options_chain
        try:
            df, S_live = fetch_options_chain('AAPL')
            return df, S_live
        except Exception as e:
            return None, None

    df_iv, S_live = load_iv_data()

    if df_iv is None or len(df_iv) == 0:
        st.error("Could not fetch options data. Yahoo Finance may be rate-limiting. Try again in a few minutes.")
    else:
        st.success(f"Loaded {len(df_iv)} options across {df_iv['expiry'].nunique()} expiries. Current AAPL: ${S_live:.2f}")

        # --- 3D Plotly surface ---
        fig_3d = go.Figure()
        expiries = sorted(df_iv['expiry'].unique())

        for i, expiry in enumerate(expiries):
            subset = df_iv[df_iv['expiry'] == expiry].sort_values('strike')
            if len(subset) < 4:
                continue
            T_val = subset['T'].iloc[0]

            fig_3d.add_trace(go.Scatter3d(
                x=subset['strike'].values,
                y=np.full(len(subset), T_val),
                z=subset['iv'].values * 100,
                mode='lines+markers',
                marker=dict(size=2),
                line=dict(width=4),
                name=f'T={T_val:.2f}y ({expiry})'
            ))

        fig_3d.update_layout(
            title="AAPL Implied Volatility Surface — Each ribbon is one expiry date",
            scene=dict(
                xaxis_title="Strike Price",
                yaxis_title="Time to Expiry (years)",
                zaxis_title="Implied Volatility (%)",
                camera=dict(eye=dict(x=1.5, y=-1.5, z=0.8))
            ),
            height=600
        )
        st.plotly_chart(fig_3d, use_container_width=True)

        # --- Smile plot for nearest expiry ---
        st.subheader("Volatility Smile — Nearest Expiry")
        nearest = sorted(expiries)[0]
        smile_data = df_iv[df_iv['expiry'] == nearest].sort_values('strike')

        fig_smile = go.Figure()
        fig_smile.add_trace(go.Scatter(
            x=smile_data['strike'], y=smile_data['iv'] * 100,
            mode='lines+markers',
            line=dict(color='steelblue', width=2),
            name='Implied Volatility'
        ))
        fig_smile.add_vline(
            x=S_live, line_dash='dash', line_color='orange',
            annotation_text=f"Current AAPL ${S_live:.1f}"
        )
        fig_smile.update_layout(
            title=f"Volatility Smile — Expiry: {nearest} | Black-Scholes assumes the flat line; markets disagree",
            xaxis_title="Strike Price",
            yaxis_title="Implied Volatility (%)",
            height=400
        )
        st.plotly_chart(fig_smile, use_container_width=True)

        st.markdown("""
        **The volatility smile shows that options away from the current stock price 
        have higher implied volatility than at-the-money options.**
        
        This contradicts Black-Scholes's core assumption of constant volatility.
        The market is pricing in 'fat tails' — extreme moves are considered more 
        likely than the lognormal distribution predicts.
        
        This is the most important empirical finding in derivatives pricing.
        """)