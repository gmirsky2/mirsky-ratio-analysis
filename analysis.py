# analysis.py
#
# This script reproduces the empirical analysis for the paper:
# "The Mirsky Ratio: An Empirical Study on the Predictive Power of R&D to SG&A Allocation"
# by Gilbert Mirsky.
#
# The script performs the following steps:
# 1. Defines a static universe of S&P 100 tickers for reproducibility.
# 2. For each ticker, it fetches annual financial data (R&D, SG&A) and 1-year stock price history.
# 3. Calculates the Mirsky Ratio (R&D / SG&A) and 1-year market growth.
# 4. Filters out companies with incomplete data.
# 5. Computes the Pearson correlation coefficient and p-value between the Mirsky Ratio and market growth.
# 6. Prints the final statistical results and saves the detailed data to a CSV file.

import yfinance as yf
import pandas as pd
from scipy.stats import pearsonr
import warnings

# Suppress minor yfinance warnings
warnings.filterwarnings("ignore")

def extract_scalar(value):
    """
    Sanitizes data from yfinance, which can be a Series, into a clean float.
    Returns 0.0 if the value cannot be converted.
    """
    try:
        if isinstance(value, pd.Series):
            value = value.iloc[0]
        return float(value)
    except (ValueError, TypeError, IndexError):
        return 0.0

def run_analysis():
    """Main function to perform the data collection and statistical analysis."""
    
    # Static S&P 100 ticker list as of the original analysis period.
    # Using a static list ensures that the original study can be precisely reproduced.
    sp100_tickers = [
        'AAPL', 'MSFT', 'GOOG', 'AMZN', 'NVDA', 'META', 'TSLA', 'BRK-B', 'LLY', 'V', 'JPM', 'XOM',
        'WMT', 'UNH', 'MA', 'PG', 'JNJ', 'MRK', 'HD', 'COST', 'AVGO', 'ORCL', 'CVX', 'CRM', 'PEP',
        'KO', 'ABBV', 'ADBE', 'BAC', 'MCD', 'CSCO', 'ACN', 'TMO', 'PFE', 'LIN', 'NFLX', 'ABT',
        'AMD', 'DIS', 'WFC', 'CMCSA', 'INTC', 'VZ', 'DHR', 'NEE', 'PM', 'UPS', 'TXN', 'RTX',
        'HON', 'AMGN', 'UNP', 'LOW', 'COP', 'IBM', 'PLD', 'SPGI', 'CAT', 'GS', 'SBUX', 'DE',
        'BLK', 'ISRG', 'LMT', 'GE', 'MDLZ', 'BA', 'TJX', 'T', 'AXP', 'AMT', 'C', 'NOW', 'PYPL',
        'SCHW', 'ZTS', 'ADI', 'CVS', 'DUK', 'EOG', 'SO', 'MMC', 'PNC', 'TGT', 'BDX', 'GILD',
        'MO', 'USB', 'ADP', 'CI', 'CSX', 'FISV', 'GM', 'HCA', 'ITW', 'KMB', 'MD', 'MMM', 'PGR',
        'SHW', 'SYK', 'ANTM'
    ]

    print("Starting analysis for companies in the S&P 100 universe...")
    
    results = []
    total_tickers = len(sp100_tickers)

    for i, ticker in enumerate(sp100_tickers):
        print(f"Processing ({i+1}/{total_tickers}): {ticker:<7}...", end=" ")
        
        try:
            stock = yf.Ticker(ticker)
            
            # Fetch 1-year price history
            hist = stock.history(period="1y")
            if len(hist) < 2:  # Need at least a start and end point
                print("SKIPPED (Insufficient price data)")
                continue

            start_price = extract_scalar(hist['Close'].iloc[0])
            end_price = extract_scalar(hist['Close'].iloc[-1])
            market_growth = ((end_price - start_price) / start_price) * 100 if start_price > 0 else 0

            # Fetch financial statements
            financials = stock.financials
            if financials.empty or 'Research And Development' not in financials.index or 'Selling General And Administration' not in financials.index:
                print("SKIPPED (Missing required financial data)")
                continue

            # Calculate the Mirsky Ratio
            rnd = extract_scalar(financials.loc['Research And Development'])
            sga = extract_scalar(financials.loc['Selling General And Administration'])

            if sga == 0:
                print("SKIPPED (SG&A is zero)")
                continue
            
            mirsky_ratio = rnd / sga
            
            results.append({
                'Ticker': ticker,
                'Mirsky_Ratio': mirsky_ratio,
                'Market_Growth_1Y_Percent': market_growth,
                'R&D': rnd,
                'SG&A': sga
            })
            print("OK")
            
        except Exception as e:
            print(f"ERROR ({e})")
            continue

    # --- Final Analysis ---
    if not results:
        print("\nNo data collected. Cannot perform analysis.")
        return

    df = pd.DataFrame(results).dropna()
    df = df.sort_values(by='Mirsky_Ratio', ascending=False).reset_index(drop=True)

    # Save results to CSV for inspection and verification
    output_filename = 'mirsky_ratio_results.csv'
    df.to_csv(output_filename, index=False)
    print(f"\nAnalysis complete. Detailed results saved to '{output_filename}'")
    
    # Perform statistical test if enough data is available
    if len(df) > 2:
        correlation, p_value = pearsonr(df['Mirsky_Ratio'], df['Market_Growth_1Y_Percent'])
        
        print("\n--- Statistical Results ---")
        print(f"Sample Size (n): {len(df)}")
        print(f"Correlation Coefficient (r): {correlation:.4f}")
        print(f"p-value: {p_value:.4f}")
        print("---------------------------")
    else:
        print("\n--- Insufficient data for statistical analysis ---")

if __name__ == "__main__":
    run_analysis()