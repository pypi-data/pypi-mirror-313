import pandas as pd

from utils import StatsFetcher

pd.options.display.max_rows = 4
pd.options.display.max_columns = 4

if __name__ == "__main__":
    import pprint
    pp = pprint.PrettyPrinter(indent=2)

    ticker = "2330"
    start_date = "2018-01-01"
    end_date = "2199-12-31"

    fetcher = StatsFetcher()

    # pp.pprint(fetcher.query_seasonal_data(ticker, start_date, end_date, 'balance_sheet'))
    # fetcher.get_balance_sheet(ticker)
    query_data = fetcher.get_profit_lose(ticker)
    print("{")
    for key, value in query_data.items():
        print(f"\t\"{key}\":")

        print(f"{value}")
    print("}")
    # pp.pprint(fetcher.get_balance_sheet(ticker))