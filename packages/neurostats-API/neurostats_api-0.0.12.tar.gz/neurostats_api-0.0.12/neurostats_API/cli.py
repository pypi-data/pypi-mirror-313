import argparse
import pprint
from fetchers.value_invest import ValueFetcher
import pandas as pd
pp = pprint.PrettyPrinter(
    indent = 2
)

pd.options.display.max_rows = 4
pd.options.display.max_columns = 4

def main():
    parser = argparse.ArgumentParser(
        prog="Neurostats Datasets fetching",
        description="Main function of fetching Neurostat Dataset",
    )    
    
    parser.add_argument("--ticker", type=str, default="2330")
    parser.add_argument("--start_date", type=str, default="2018-01-01")
    parser.add_argument("--end_date", type=str, default="2199-12-31")

    args = parser.parse_args()

    fetcher = ValueFetcher(args.ticker)

    query_data = fetcher.query_data()
    print("{")
    for key, value in query_data.items():
        print(f"\t\"{key}\":")

        print(f"{value}")
    print("}")

if (__name__ == "__main__"):
    main()