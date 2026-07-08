import numpy as np 
import matplotlib.pyplot as plt 
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm 
import pandas as pd 
from implied_volatility import fetch_options_chain 

def plot_volatility_smile(df, S, expiry_index=0, save_path='volatility_smile.png'):
    """
    Plot IV vs strike for a single expiry date.
    Should show a U-shaped smile- higher IV for deep OTM/ITM options.
    At-the-money (strike near S) should have the lowest IV.
    """
    expiries= sorted(df['expiry'].unique())
    if expiry_index>=len(expiries):
        expiry_index=0

    chosen_expiry= expiries[expiry_index]
    subset= df[df['expiry']==chosen_expiry].sort_values('strike')
    T_label= subset['T'].iloc[0]

    fig, ax= plt.subplots(figsize=(10,5))

    ax.plot(subset['strike'], subset['iv']*100, '-o', color='steelblue', linewidth=2,
    markersize=5, label= f'IV- expiry: {chosen_expiry}')

    #mark the ATM point (strike closest to the current price)
    atm_idx= (subset['strike']-S).abs().idxmin()
    atm_row= subset.loc[atm_idx]
    ax.axvline(x=S, color='orange', linestyle='--', linewidth=1.5,
               label=f'Current price S = ${S:.1f}')
    ax.scatter([atm_row['strike']], [atm_row['iv'] * 100],
               s=100, color='orange', zorder=5,
               label=f"ATM IV ≈ {atm_row['iv']:.1%}")

    ax.set_xlabel('Strike Price (K)', fontsize=12)
    ax.set_ylabel('Implied Volatility (%)', fontsize=12)
    ax.set_title(
        f'Volatility Smile — AAPL Options (T = {T_label:.2f} years)\n'
        f'Evidence that markets price fat tails beyond Black-Scholes',
        fontsize=12
    )
    ax.legend(fontsize=10)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(save_path, dpi=150)
    plt.show()
    print(f"Smile plot saved to {save_path}")

def plot_volatility_surface(df, S, save_path='volatility_surface.png'):
    """
    Plot 3D volatility surface: IV vs Strike vs Time to Expiry.
    Each ribbon is one expiry date. Together they form the surface.
    """
    fig = plt.figure(figsize=(12, 7))
    ax = fig.add_subplot(111, projection='3d')

    expiries = sorted(df['expiry'].unique())
    colours = cm.viridis(np.linspace(0, 1, len(expiries)))

    for i, expiry in enumerate(expiries):
        subset = df[df['expiry'] == expiry].sort_values('strike')
        if len(subset) < 4:
            continue

        strikes = subset['strike'].values
        ivs     = subset['iv'].values * 100    # convert to %
        T_val   = subset['T'].iloc[0]
        T_arr   = np.full_like(strikes, T_val)

        ax.plot(strikes, T_arr, ivs,
                color=colours[i], linewidth=1.8, alpha=0.85,
                label=f'T={T_val:.2f}y')

    ax.set_xlabel('Strike Price', fontsize=10)
    ax.set_ylabel('Time to Expiry (years)', fontsize=10)
    ax.set_zlabel('Implied Volatility (%)', fontsize=10)
    ax.set_title(
        'SPY Volatility Surface\n'
        'Each ribbon = one expiry. Colour = time (dark=short, light=long)',
        fontsize=11
    )
    ax.view_init(elev=25, azim=-60)
    ax.legend(fontsize=7, loc='upper left')
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    plt.show()
    print(f"Surface plot saved to {save_path}")


if __name__ == '__main__':
    df, S = fetch_options_chain('SPY')

    print("\nGenerating volatility smile...")
    plot_volatility_smile(df, S, expiry_index=1)

    print("Generating 3D volatility surface...")
    plot_volatility_surface(df, S)