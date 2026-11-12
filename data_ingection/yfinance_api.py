import yfinance as yf
import pandas as pd

symbols = pd.read_csv("symbols.txt" , sep=",")
print(symbols)
print("="*100)
for s in symbols:
	print(yf.Ticker(s))
	print("-"*100)



