import yfinance as yf

def test():
    l = {}
    
    # 1. Read the file using standard Python
    with open("symbols.txt", "r") as file:
        raw_data = file.read()
        
    # 2. Split by comma and clean up the symbols (removes spaces and '$')
    symbols = [symbol.strip().replace('$', '') for symbol in raw_data.split(',')]
    
    # 3. Iterate through the cleaned symbols
    for s in symbols:
        if not s:  # Skip any empty strings resulting from trailing commas
            continue
            
        try:
            # Fetch the price
            l[s] = yf.Ticker(s).fast_info['lastPrice']
            print(f"Successfully fetched {s}: {l[s]}")
        except Exception as e:
            print(f"Failed to fetch data for {s}: {e}")
            
    return l