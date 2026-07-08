import yfinance as yf

stock = yf.Ticker("AAPL")

# Check 1: Can you get the current price?
hist = stock.history(period="1d")
print("Price data shape:", hist.shape)
print("Current price:", hist['Close'].iloc[-1] if not hist.empty else "EMPTY")

# Check 2: Can you get expiry dates?
print("Options expiries:", stock.options)

# Check 3: If expiries exist, can you get the chain?
if stock.options:
    expiry = stock.options[0]
    print("Trying expiry:", expiry)
    chain = stock.option_chain(expiry)
    print("Calls shape:", chain.calls.shape)
    print("Calls columns:", chain.calls.columns.tolist())
    print("First 3 rows of calls:")
    print(chain.calls[['strike', 'bid', 'ask', 'lastPrice']].head(3))