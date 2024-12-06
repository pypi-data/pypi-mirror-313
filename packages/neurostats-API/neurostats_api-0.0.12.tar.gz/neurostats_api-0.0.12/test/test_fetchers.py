import json
from pprint import PrettyPrinter
import pytest
import pandas as pd
import yaml
from neurostats_API.utils import StatsProcessor, DBClient

pd.set_option('display.max_rows', 5)
pd.set_option('display.max_columns', 4)

pp = PrettyPrinter(
    indent=2
)

with open(f"./neurostats_API/tw50_company_list.json") as f:
    company_list = json.load(f)
db_client = DBClient("mongodb://neurowatt:neurodb123@db.neurowatt.ai:27017/neurowatt").get_client()

def test_value():
    from neurostats_API.fetchers import ValueFetcher
    for ticker in company_list.keys():
    
        fetcher = ValueFetcher(ticker=ticker, db_client=db_client)

        fetched_data = fetcher.query_data()
    

    assert ('daily_data' in fetched_data)
    assert ('yearly_data' in fetched_data)

    assert isinstance(fetched_data['daily_data'], dict)
    assert isinstance(fetched_data['yearly_data'], pd.DataFrame)
    print("============================VALUE INVEST\n")
    for key, item in fetched_data.items():
        print(f"\"{key}\":\n{item}")
    

def test_profit_lose():
    from neurostats_API.fetchers import ProfitLoseFetcher

    for ticker in company_list.keys():
    
        fetcher = ProfitLoseFetcher(ticker, db_client)

        data = fetcher.query_data()

    table_settings = StatsProcessor.load_yaml("profit_lose.yaml")
    
    for key in table_settings.keys():
        assert key in data.keys()
    print("============================PROFIT LOSE\n")
    for key, item in data.items():
        print(f"\"{key}\":\n{item}")

def test_cash_flow():
    from neurostats_API.fetchers import CashFlowFetcher

    for ticker in company_list.keys():
        
        fetcher = CashFlowFetcher(ticker, db_client)
        data = fetcher.query_data()

    assert("cash_flow" in data.keys())
    assert("CASHO" in data.keys())
    assert("CASHI" in data.keys())
    assert("CASHF" in data.keys())

    print("============================CASH FLOW: \n")
    for key, item in data.items():
        print(f"\"{key}\":\n{item}")

def test_month_revenue():
    from neurostats_API.fetchers import MonthRevenueFetcher
    for ticker in company_list.keys():
    
        fetcher = MonthRevenueFetcher(ticker, db_client)
        data = fetcher.query_data()

    assert("month_revenue" in data.keys())
    assert("this_month_revenue_over_years" in data.keys())
    assert("grand_total_over_years" in data.keys())
    print("============================Month Revenue:\n")
    for key, item in data.items():
        print(f"\"{key}\":\n{item}")


def test_balance_sheet():
    from neurostats_API.fetchers import BalanceSheetFetcher
    for ticker in company_list.keys():
        
        fetcher = BalanceSheetFetcher(ticker=ticker, db_client=db_client)

        data = fetcher.query_data()
        
    assert("balance_sheet" in data.keys())
    assert('total_asset' in data.keys())
    assert('current_asset' in data.keys())
    assert('non_current_asset' in data.keys())
    assert('current_debt' in data.keys())
    assert('non_current_debt' in data.keys())
    assert('equity' in data.keys())
    print("============================BALANCE SHEET:\n")
    for key, item in data.items():
        print(f"\"{key}\":\n{item}")

def test_finance_overview():
    from neurostats_API.fetchers import FinanceOverviewFetcher
    company_list = {"2330": "台積電"}
    for ticker in company_list.keys():
        fetcher = FinanceOverviewFetcher(ticker=ticker, db_client=db_client)
        fetched_data = fetcher.query_data()

        # except Exception as e:
        #     print(f"{ticker} finance_overview {str(e)}")

    expected_keys = [
    # Queried items
        'revenue',
        'gross_profit',
        'operating_income',
        'net_income',
        'operating_cash_flow',
        'invest_cash_flow',
        'financing_cash_flow',
        'capital',
        'eps',
        'total_assets',
        'equity',
        'net_income_before_tax',
        'interest',
        'operating_expenses',
        'net_income_rate',
        'revenue_YoY',
        'gross_prof_YoY',
        'operating_income_YoY',
        'net_income_YoY',
        'account_receive',
        'account_pay',
        'inventories',
        'operating_cost',
        'application',
        'current_assets',
        'current_liabilities',
        'total_liabilities',
        'cash_and_cash_equivalents',
        'interest_expense',

        # calculated_items
        'fcf',
        'EBIT',
        'share_outstanding',
        'revenue_per_share',
        'gross_per_share',
        'operating_income_per_share',
        'operating_cash_flow_per_share',
        'fcf_per_share',
        'roa',
        'roe',
        'gross_over_asset',
        'roce',
        'gross_profit_margin',
        'operation_profit_rate',
        'operating_cash_flow_profit_rate',
        'dso',
        'account_receive_over_revenue',
        'dpo',
        'inventories_cycle_ratio',
        'dio',
        'inventories_revenue_ratio',
        'cash_of_conversion_cycle',
        'asset_turnover',
        'application_turnover',
        'current_ratio',
        'quick_ratio',
        'debt_to_equity_ratio',
        'net_debt_to_equity_ratio',
        'interest_coverage_ratio',
        'debt_to_operating_cash_flow',
        'debt_to_free_cash_flow',
        'cash_flow_ratio',
    ]

    for key in expected_keys:
        assert key in fetched_data['seasonal_data'], f"{key} not found in fetched_data"
        # assert fetched_data['seasonal_data'][0][key] is not None, f"{key} is None"

    pp.pprint(fetched_data)

def test_institution_trading():
    from neurostats_API.fetchers import InstitutionFetcher
    fetcher = InstitutionFetcher(ticker='2330', db_client = db_client)

    fetched_data = fetcher.query_data()

    pp.pprint(fetched_data)

def test_margin_trading():
    from neurostats_API.fetchers import MarginTradingFetcher
    fetcher = MarginTradingFetcher(ticker='2330', db_client=db_client)

    fetched_data = fetcher.query_data()

    pp.pprint(fetched_data)