import pandas as pd
import json
import pytz
from datetime import datetime, timedelta, date
from .data_process import StatsProcessor
import yaml


class StatsFetcher:

    def __init__(self, db_client):
        self.db = db_client["company"]  # Replace with your database name
        self.collection = self.db["twse_stats"]

        self.timezone = pytz.timezone("Asia/Taipei")

        self.inverse_dict = StatsProcessor.load_txt("seasonal_data_field_dict.txt", json_load=True)

        self.seasons = ["01", "02", "03", "04"]

        self.pipeline = list()

        self.target_metric_dict = {
            'value': ['value'],
            'value_and_percentage': ['value', 'percentage'],
            'percentage': ['percentage'],
            'grand_total': ['grand_total'],
            'grand_total_values':['grand_total', 'grand_total_percentage'],
            'grand_total_percentage':['grand_total_percentage'],
            'growth': [f'YoY_{i}' for i in [1,3,5,10]],
            'grand_total_growth': [f"YoY_{i}" for i in [1,3,5,10]]
        }

        self.__return_dict = dict()

    def _flush_dict(self):
        self.__return_dict = dict()

    def _default_query(self, ticker, start_date, end_date):

        start_year, start_month, start_day = [
            int(num) for num in start_date.split("-")
        ]
        end_year, end_month, end_day = [
            int(num) for num in end_date.split("-")
        ]

        start_date = datetime.strptime(start_date, "%Y-%m-%d")
        end_date = datetime.strptime(end_date, "%Y-%m-%d")
        start_date = self.timezone.localize(start_date)
        end_date = self.timezone.localize(end_date)

        start_season = start_month // 3 + 1
        end_season = end_month // 3 + 1

        ticker = ticker.strip().split()[0]

        self.pipeline = [
            # 1. Find Ticker
            {
                "$match": {
                    "ticker": ticker,
                }
            },
            # 2. Find by date
            {
                "$project": {
                    "ticker": 1,
                    "company_name": 1,
                    # 2.1 Filter monthly_data
                    "daily_data": {
                        "$filter": {
                            "input": "$daily_data",
                            "as": "daily",
                            "cond": {
                                "$and": [
                                    {
                                        "$gte": ["$$daily.date", start_date]
                                    },
                                    {
                                        "$lte": ["$$daily.date", end_date]
                                    },
                                ]
                            },
                        }
                    },
                    # 2.2 Filter monthly_data
                    "monthly_data": {
                        "$filter": {
                            "input": "$monthly_data",
                            "as": "monthly",
                            "cond": {
                                "$or": [
                                    {
                                        "$and": [
                                            {
                                                "$eq":
                                                ["$$monthly.year", start_year]
                                            },
                                            {
                                                "$gte": [
                                                    "$$monthly.month",
                                                    start_month
                                                ]
                                            },
                                        ]
                                    },
                                    {
                                        "$and": [
                                            {
                                                "$eq":
                                                ["$$monthly.year", end_year]
                                            },
                                            {
                                                "$lte":
                                                ["$$monthly.month", end_month]
                                            },
                                        ]
                                    },
                                    {
                                        "$and": [
                                            {
                                                "$gt":
                                                ["$$monthly.year", start_year]
                                            },
                                            {
                                                "$lt":
                                                ["$$monthly.year", end_year]
                                            },
                                        ]
                                    },
                                ]
                            },
                        }
                    },
                    # 2.3 Filter seasonal_data
                    "seasonal_data": {
                        "$filter": {
                            "input": "$seasonal_data",
                            "as": "seasonal",
                            "cond": {
                                "$or": [
                                    {
                                        "$and": [
                                            {
                                                "$eq": [
                                                    "$$seasonal.year",
                                                    start_year
                                                ]
                                            },
                                            {
                                                "$gte": [
                                                    "$$seasonal.season",
                                                    start_season
                                                ]
                                            },
                                        ]
                                    },
                                    {
                                        "$and": [
                                            {
                                                "$eq":
                                                ["$$seasonal.year", end_year]
                                            },
                                            {
                                                "$lte": [
                                                    "$$seasonal.season",
                                                    end_season
                                                ]
                                            },
                                        ]
                                    },
                                    {
                                        "$and": [
                                            {
                                                "$gt": [
                                                    "$$seasonal.year",
                                                    start_year
                                                ]
                                            },
                                            {
                                                "$lt":
                                                ["$$seasonal.year", end_year]
                                            },
                                        ]
                                    },
                                ]
                            },
                        }
                    },
                    "yearly_data": {
                        "$filter": {
                            "input": "$yearly_data",
                            "as": "yearly",
                            "cond": {
                                "$and": [
                                    {
                                        "$gte": ["$$yearly.year", 107]
                                    },
                                    {
                                        "$lte": ["$$yearly.year", end_year]
                                    },
                                ]
                            },
                        }
                    }
                }
            },
        ]

    def query_data(self, ticker, start_date, end_date):
        """
        Return : Dict {
                    'ticker' : <ticker>,
                    'company_name': <company_name>,
                    'daily_data': List[Dict]
                    'monthly_data': List[Dict]
                    'seasonal_data': List[Dict]
                }
        """

        self._default_query(ticker, start_date, end_date)

        fetched_datas = list(self.collection.aggregate(self.pipeline))

        return fetched_datas[0]

    def query_values(self, ticker, start_date, end_date):
        self._default_query(ticker, start_date, end_date)

        self.pipeline.append({
            "$project": {
                "ticker": 1,
                "company_name": 1,

                # Transform daily_data to include only index and date
                "daily_data": {
                    "$map": {
                        "input": "$daily_data",
                        "as": "daily_item",
                        "in": {
                            "date": "$$daily_item.date",
                            "close": "$$daily_item.close",
                            "P_B": "$$daily_item.P_B",
                            "P_E": "$$daily_item.P_E",
                            "P_FCF": "$$daily_item.P_FCF",
                            "P_S": "$$daily_item.P_S",
                            "EV_OPI": "$$daily_item.EV_OPI",
                            "EV_EBIT": "$$daily_item.EV_EBIT",
                            "EV_EBITDA": "$$daily_item.EV_EBITDA",
                            "EV_S": "$$daily_item.EV_S"
                        }
                    }
                },
                "yearly_data": 1
            }
        })

        fetched_datas = list(self.collection.aggregate(self.pipeline))

        return fetched_datas[0]

    def query_stock_price(self, ticker, start_date, end_date):

        self.pipeline.append({
            "$project": {
                "ticker": 1,
                "company_name": 1,

                # Transform daily_data to include only index and date
                "daily_data": {
                    "$map": {
                        "input": "$daily_data",
                        "as": "daily_item",
                        "in": {
                            "date": "$$daily_item.date",
                            "open": "$$daily_item.open",
                            "high": "$$daily_item.high",
                            "los": "$$daily_item.low",
                            "close": "$$daily_item.close",
                        }
                    }
                },
            }
        })

        fetched_datas = list(self.collection.aggregate(self.pipeline))

        return fetched_datas[0]

    def query_seasonal_data(self, ticker, start_date, end_date, sheet, target_season):

        self._default_query(ticker, start_date, end_date)
        self.pipeline.append({
            "$project": {
                "ticker": 1,
                "company_name": 1,
                "seasonal_data": {
                    "$filter":{
                        "input":{
                            "$map": {
                                "input": "$seasonal_data",
                                "as": "seasonal_item",
                                "in": {
                                    "year": "$$seasonal_item.year",
                                    "season": "$$seasonal_item.season",
                                    f"{sheet}": f"$$seasonal_item.{sheet}"
                                }
                            }
                        },
                        "as": "filtered_item",
                        "cond": { "$eq": ["$$filtered_item.season", target_season] }
                    }
                },
            }
        })

        self.pipeline.append({"$unwind": "$seasonal_data"})

        self.pipeline.append(
            {"$sort": {
                "seasonal_data.year": 1,
                "seasonal_data.season": 1
            }})

        fetched_datas = list(self.collection.aggregate(self.pipeline))

        return fetched_datas

    def query_month_revenue(self, ticker, start_date, end_date):
        self._default_query(ticker, start_date, end_date)
        self.pipeline.append(
            {
                "$project": {
                    "ticker": 1,
                    "company_name": 1,
                    "monthly_data": {
                        "$sortArray": {
                            "input": "$monthly_data",
                            "sortBy": {
                                "year": 1,
                                "month": 1
                            }
                        }
                    },
                }
            }, )

        fetched_datas = list(self.collection.aggregate(self.pipeline))

        return fetched_datas[0]

    def query_latest_values(self, ticker):
        """
        傳回最近一天的價值面

        return : Dict {
            "ticker": 股票代碼,
            "company_name": 公司中文名稱,
        ## 以下八個是iFa項目
            "P_E": 本益比,
            "P_B": 股價,
            "P_FCF": 股價自由現金流比,
            "P_S": 股價營收比,
            "EV_EBIT: ,
            "EV_EBITDA": ,
            "EV_OPI": ,
            "EV_S"; ,
        ## 以上八個是iFa項目
            "close": 收盤價,
            "EV": 市場價值
        }
        """
        today = date.today()
        yesterday = (today - timedelta(days=14)).strftime("%Y-%m-%d")
        today = today.strftime("%Y-%m-%d")

        fetched_datas = self.query_values(ticker, yesterday, today)

        daily_data = fetched_datas.pop('daily_data')
        fetched_datas.update(daily_data[-1])
        return fetched_datas

    def query_latest_month_revenue(self, ticker):
        """
        傳回最新一期的月營收
        """

        today = date.today()

        last_month = (today - timedelta(days=30)).strftime("%Y-%m-%d")
        today = today.strftime("%Y-%m-%d")

        fetched_datas = self.query_month_revenue(ticker, last_month, today)

        print(fetched_datas)

        latest_month_revenue = fetched_datas['monthly_data']
        fetched_datas.pop('monthly_data')

        fetched_datas.update(latest_month_revenue[-1])

        return fetched_datas

    def query_latest_seasonal_data(self, ticker):
        """
        傳回最新一期的季報
        """
        today = date.today()

        last_season = (today - timedelta(days=90)).strftime("%Y-%m-%d")
        today = today.strftime("%Y-%m-%d")

        fetched_datas = self.query_seasonal_data(ticker, last_season, today)

        print(fetched_datas)

        latest_seasonal_data = fetched_datas['seasonal_data']
        fetched_datas.pop('seasonal_data')

        fetched_datas.update(latest_seasonal_data[-1])

        return fetched_datas

    def get_value_sheet(self, ticker):
        """
        iFa.ai: 價值投資-> 市場指標
        """
        """
        傳回最近一天的價值面

        return : Dict {
            "ticker": 股票代碼,
            "company_name": 公司中文名稱,
            "daily_data":{
            ## 以下八個是iFa項目
                "P_E": 本益比,
                "P_B": 股價,
                "P_FCF": 股價自由現金流比,
                "P_S": 股價營收比,
                "EV_EBIT: ,
                "EV_EBITDA": ,
                "EV_OPI": ,
                "EV_S"; 
            ## 以上八個是iFa項目
                "close": 收盤價,
            }

            "yearly_data": pd.DataFrame (下表格為範例)
                year    P_E       P_FCF   P_B        P_S     EV_OPI    EV_EBIT   EV_EBITDA       EV_S
            0   107  16.68   29.155555  3.71  11.369868  29.837201  28.798274  187.647704  11.107886
            1   108  26.06   67.269095  5.41  17.025721  50.145736  47.853790  302.526388  17.088863
            2   109  27.98   95.650723  7.69  22.055379  53.346615  51.653834  205.847232  22.481951
            3   110  27.83  149.512474  7.68  22.047422  55.398018  54.221387  257.091893  22.615355
            4   111  13.11   48.562021  4.25  11.524975  24.683850  24.226554   66.953260  12.129333
            5   112  17.17  216.371410  4.59  16.419533  40.017707  37.699267  105.980652  17.127656
        }
        """
        today = date.today()
        this_year = today.year - 1911
        yesterday = (today - timedelta(days=14)).strftime("%Y-%m-%d")
        today = today.strftime("%Y-%m-%d")

        fetched_datas = self.query_values(ticker, yesterday, today)

        fetched_datas['daily_data'] = fetched_datas['daily_data'][-1]

        latest_data = {"year": f"過去4季"}

        latest_data.update(fetched_datas['daily_data'])
        latest_data.pop("date")
        latest_data.pop("close")

        fetched_datas['yearly_data'].append(latest_data)

        fetched_datas['yearly_data'] = pd.DataFrame.from_dict(
            fetched_datas['yearly_data'])

        return fetched_datas

    def get_month_revenue_sheet(self, ticker):
        """
        iFa.ai: 財務分析 -> 每月營收

        return: Dict {
            'ticker': str,
            'company_name': str,
            'month_revenue': pd.DataFrame  (歷年的月營收以及到今年最新月份累計的月營收表格)
            'this_month_revenue_over_years': pd.DataFrame (今年這個月的月營收與歷年同月份的營收比較)
            'grand_total_over_years': pd.DataFrame (累計至今年這個月的月營收與歷年的比較)
        }
        """

        today = datetime.today()
        today = today.strftime("%Y-%m-%d")

        start_date = "2014-01-01"

        query_data = self.query_month_revenue(ticker, start_date, today)

        monthly_data = query_data['monthly_data']

        this_month = monthly_data[-1]["month"]

        month_dict = {i: None for i in range(1, 13)}
        month_dict[f"grand_total"] = None

        monthly_dict = dict()

        revenue_by_year = dict()
        single_month_revenue_dict = {
            "revenue": None,
            "MoM": None,
            "YoY": None,
            "YoY_3": None,
            "YoY_5": None,
            "YoY_10": None
        }

        grand_total_by_year = dict()
        grand_total_dict = {
            "revenue": None,
            "MoM": None,
            "YoY": None,
            "YoY_3": None,
            "YoY_5": None,
            "YoY_10": None
        }

        for data in monthly_data:
            try:
                monthly_dict[data['year']][data['month']] = data['revenue']
            except:
                monthly_dict[data['year']] = month_dict.copy()
                monthly_dict[data['year']][data['month']] = data['revenue']

            try:
                if (data['last_year_revenue']
                        != monthly_dict[data['year'] - 1][data['month']]):
                    monthly_dict[data['year'] -
                                 1][data['month']] = data['last_year_revenue']
            except:
                pass

            if (data['month'] == this_month):
                monthly_dict[
                    data['year']][f"grand_total"] = data['grand_total']

                single_month_revenue_dict['revenue'] = data["revenue"]
                single_month_revenue_dict['YoY'] = data[
                    "revenue_increment_ratio"]

                grand_total_dict['revenue'] = data["grand_total"]
                grand_total_dict['YoY'] = data['grand_total_increment_ratio']

                revenue_by_year[
                    data['year']] = single_month_revenue_dict.copy()
                grand_total_by_year[data['year']] = grand_total_dict.copy()

        query_data['month_revenue'] = pd.DataFrame(monthly_dict)
        query_data['this_month_revenue_over_years'] = pd.DataFrame(
            revenue_by_year)
        query_data['grand_total_over_years'] = pd.DataFrame(
            grand_total_by_year)

        query_data.pop("monthly_data")

        return query_data

    def _expand_value_percentage(self, dataframe):

        expanded_columns = {}
        for col in dataframe.columns:
            # Use json_normalize to split 'value' and 'percentage'
            expanded_df = pd.json_normalize(
                dataframe[col]).add_prefix(f"{col}_")
            expanded_df.index = dataframe.index
            # Append the expanded columns to the new DataFrame
            expanded_columns[col] = expanded_df

        expanded_df = pd.concat(expanded_columns.values(), axis=1)

        return expanded_df

    def _get_today(self):
        today = datetime.today()
        this_year = today.year
        this_month = today.month
        this_day = today.day

        return {
            "today": today,
            "year": this_year,
            "month": this_month,
            "day": this_day,
        }

    def get_balance_sheet(self, ticker):
        """
        iFa.ai: 財務分析 -> 資產負債表

        Return: Dict
        {
            'ticker': 股票代碼,
            'company_name': 公司名稱,

            'balance_sheet': 歷年當季資場負債表"全表" (pd.DataFrame)
            'total_asset': 歷年當季資產總額 (pd.DataFrame)
            'current_asset': 歷年當季流動資產總額 (pd.DataFrame)
            'non_current_asset': 歷年當季非流動資產 (pd.DataFrame)
            'current_debt': 歷年當季流動負債 (pd.DataFrame)
            'non_current_debt': 歷年當季非流動負債 (pd.DataFrame)
            'equity': : 歷年當季權益 (pd.DataFrame)
        }
        """
        today_dict = self._get_today()

        today = today_dict['today']
        target_season = ((today.month - 1) // 3) + 1

        start_date = "2014-01-01"
        end_date = today.strftime("%Y-%m-%d")

        query_data = self.query_seasonal_data(ticker, start_date, end_date,
                                              "balance_sheet", target_season=target_season)

        return_dict = {
            "ticker": query_data[0]['ticker'],
            "company_name": query_data[0]['company_name'],
        }

        index_names = []

        table_dict = dict()
        total_asset_dict = dict()
        current_asset_dict = dict()
        non_current_asset_dict = dict()
        current_debt_dict = dict()
        non_current_debt_dict = dict()
        equity_dict = dict()

        this_season = query_data[-1]['seasonal_data']['season']

        value_type_list = ['value', 'percentage']

        for data in query_data:
            year = data['seasonal_data']['year']
            season = data['seasonal_data']['season']

            time_index = f"{year}Q{season}"

            if (season == this_season):
                try:
                    table_dict[time_index] = data['seasonal_data'][
                        'balance_sheet']
                except:
                    table_dict[time_index] = dict()
                    table_dict[time_index] = data['seasonal_data'][
                        'balance_sheet']

                try:
                    total_asset_dict[time_index] = {
                        "total_asset":
                        data['seasonal_data']['balance_sheet']['資產總額'],
                        "total_debt":
                        data['seasonal_data']['balance_sheet']['負債總額'],
                        "total_equity":
                        data['seasonal_data']['balance_sheet']['權益總額'],
                    }
                except:
                    total_asset_dict[time_index] = {
                        "total_asset": None,
                        "total_debt": None,
                        "total_equity": None,
                    }

                for value_type in value_type_list:
                    try:
                        current_asset_dict[
                            f"{time_index}_{value_type}"] = data[
                                'seasonal_data']['balance_sheet']['流動資產合計'][
                                    value_type]
                    except:
                        if (time_index not in current_asset_dict.keys()):
                            current_asset_dict[
                                f"{time_index}_{value_type}"] = None

                    try:
                        non_current_asset_dict[
                            f"{time_index}_{value_type}"] = data[
                                'seasonal_data']['balance_sheet']['非流動資產合計'][
                                    value_type]
                    except:
                        non_current_asset_dict[
                            f"{time_index}_{value_type}"] = None

                    try:
                        current_debt_dict[f"{time_index}_{value_type}"] = data[
                            'seasonal_data']['balance_sheet']['流動負債合計'][
                                value_type]
                    except:
                        current_debt_dict[f"{time_index}_{value_type}"] = None

                    try:
                        non_current_debt_dict[
                            f"{time_index}_{value_type}"] = data[
                                'seasonal_data']['balance_sheet']['非流動負債合計'][
                                    value_type]
                    except:
                        non_current_debt_dict[
                            f"{time_index}_{value_type}"] = None

                    try:
                        equity_dict[f"{time_index}_{value_type}"] = data[
                            'seasonal_data']['balance_sheet']['權益合計'][
                                value_type]
                    except:
                        equity_dict[f"{time_index}_{value_type}"] = None

                index_names += list(
                    data['seasonal_data']['balance_sheet'].keys())

        index_names = list(dict.fromkeys(index_names))

        balance_sheet_table = pd.DataFrame(table_dict)
        balance_sheet_table = self._expand_value_percentage(
            balance_sheet_table)

        total_asset_table = pd.DataFrame(total_asset_dict)
        total_asset_table = self._expand_value_percentage(total_asset_table)

        current_asset_table = pd.DataFrame(current_asset_dict,
                                           index=['current_asset'])
        non_current_asset_table = pd.DataFrame(non_current_asset_dict,
                                               index=['non_current_asset'])
        current_debt_table = pd.DataFrame(non_current_asset_dict,
                                          index=['current_debt'])
        non_current_debt_table = pd.DataFrame(non_current_asset_dict,
                                              index=['non_current_debt'])
        equity_table = pd.DataFrame(non_current_asset_dict, index=['equity'])

        return_dict['balance_sheet'] = balance_sheet_table
        return_dict['total_asset'] = total_asset_table
        return_dict['current_asset'] = current_asset_table
        return_dict['non_current_asset'] = non_current_asset_table
        return_dict['current_debt'] = current_debt_table
        return_dict['non_current_debt'] = non_current_debt_table
        return_dict['equity'] = equity_table
        return return_dict

    def _gen_dict(self,
                  query_data,
                  target_season,
                  keys,
                  calculate_type='value',
                  calculate_grand_total=False):
        """
        Will be deprecated
        """
        assert(calculate_type in ['growth_rate', 'value', 'percentage']), "args: calculate_type Error"
        table_dict = dict()
        grand_total_dict = dict() if (calculate_grand_total) else None

        for data in query_data:
            if (calculate_grand_total
                    and data['seasonal_data']['season'] <= target_season):
                time_index = f"{data['seasonal_data']['year']}Q{target_season}"
                profit_lose = data['seasonal_data']['profit_lose']

                for key in keys:
                    try:
                        if (calculate_type in ['growth_rate']):
                            for growth_rate in ['YoY_1', 'YoY_3', 'YoY_5', 'YoY_10']:
                                try:
                                    grand_total_dict[time_index][
                                        growth_rate] += profit_lose[key][growth_rate]
                                except Exception:
                                    if (time_index not in 
                                    grand_total_dict.keys()):
                                        grand_total_dict[time_index] = {
                                            "YoY": None,
                                            "YoY_3": None,
                                            "YoY_5": None,
                                            "YoY_10": None,
                                        }
                                    grand_total_dict[time_index][
                                        growth_rate] = profit_lose[key][growth_rate]

                        elif (calculate_type in ['percentage']):
                            grand_total_dict[time_index] += profit_lose[key][
                                calculate_type] / target_season
                        else:
                            grand_total_dict[time_index] += profit_lose[key][
                                calculate_type]
                        break
                    except KeyError:
                        try:
                            if (calculate_type
                                    in ['percentage']):
                                grand_total_dict[time_index] = profit_lose[
                                    key][calculate_type] / target_season
                            else:
                                grand_total_dict[time_index] = profit_lose[
                                    key][calculate_type]
                            break
                        except:  # key in profit_lose not found or not growth_rate not implemented
                            continue
                    except Exception:  # Other exceotion
                        continue
                else:  # All keys not found
                    grand_total_dict[time_index] = None

            if (data['seasonal_data']['season'] == target_season):
                time_index = f"{data['seasonal_data']['year']}Q{target_season}"
                profit_lose = data['seasonal_data']['profit_lose']

                for key in keys:
                    try:
                        if (calculate_type in ['growth_rate']):
                            for item in items:
                                table_dict[time_index][item] = profit_dict[key][item]
                        else:
                            table_dict[time_index] = profit_lose[key][
                            calculate_type]
                        break
                    except Exception:
                        continue
                else:
                    if (calculate_type == 'growth_rate'):
                        table_dict[time_index] = {
                            "YoY_1": None,
                            "YoY_3": None,
                            "YoY_5": None,
                            "YoY_10": None
                        }
                    else:
                        table_dict[time_index] = None
        return table_dict, grand_total_dict
    
    def _slice_multi_col_table(
        self,
        total_table,
        mode='value',
        target_index=None, # None or Str， 要特別抓哪個index
    ):
        times = total_table.columns.get_level_values(0).unique()
        try:
            target_metrics = self.target_metric_dict[mode]
        except KeyError as e:
            return f"mode Error: Get mode should be {list(self.target_metric_dict.keys())} but get {mode}"
        
        desired_order = [
            (time, value_name) for time in times for value_name in target_metrics
        ]

        if (target_index):
            sliced_table = total_table.loc[[target_index], pd.IndexSlice[:, target_metrics]][desired_order].T
            sliced_table = sliced_table.reset_index()
            sliced_table = sliced_table.pivot(index='level_1', columns='level_0', values=target_index)
            sliced_table.columns.name = None
            sliced_table.index.name = None
            return sliced_table.reindex(target_metrics)
        
        else:
            return total_table.loc[:, pd.IndexSlice[:, target_metrics]][desired_order]

    def get_profit_lose(self, ticker):
        """
        ticker: str
        iFa.ai: 財務分析 -> 損益表
        """
        today_dict = self._get_today()

        table_settings = StatsProcessor.load_yaml("profit_lose.yaml")
        today = today_dict['today'].strftime("%Y-%m-%d")
        start_date = "2014-01-01"

        this_season = ((today_dict['month'] - 1) // 3)
        this_season = 4 if (this_season == 0) else this_season - 1
        # TODO: 將這裡改成根據每公司的最後更新季度

        query_data = self.query_seasonal_data(ticker,
                                              start_date=start_date,
                                              end_date=today,
                                              sheet='profit_lose',
                                              target_season=this_season)

        index_names = []

        return_dict = {
            "ticker": query_data[0]['ticker'],
            "company_name": query_data[0]['company_name'],
        }

        table_dict = dict()
        grand_total_dict = dict()

        column_names = []

        for data in query_data:
            year = data['seasonal_data']['year']
            season = data['seasonal_data']['season']

            time_index = f"{year}Q{season}"

            index_names += list(
                data['seasonal_data']['profit_lose'].keys())

            profit_lose = data['seasonal_data']['profit_lose']
            
            for index_name, value_dict in profit_lose.items():
                column_names += [
                    (time_index, index_name, item_name) 
                    for item_name in value_dict.keys()
                ]
                for item_name, item in value_dict.items():
                    try:
                        table_dict[index_name][(time_index, item_name)] = item 
                        #[time_index][index_name][item_name] = item

                    except KeyError:
                        if (index_name not in table_dict.keys()):
                            table_dict[index_name] = dict()
                            grand_total_dict[index_name] = dict()
                        
                        table_dict[index_name][(time_index, item_name)] = item 

        columns = pd.MultiIndex.from_tuples(table_dict.keys())
        total_table = pd.DataFrame.from_dict(
            table_dict,
            orient='index'
        )

        total_table.columns = pd.MultiIndex.from_tuples(total_table.columns)

        for name, setting in table_settings.items():
            return_dict[name] = self._slice_multi_col_table(
                total_table=total_table,
                mode=setting['mode'],
                target_index=setting['target_index'] if "target_index" in setting.keys() else None 
            )
        
        return return_dict

    def get_cash_flow(self, ticker):
        """
        iFa.ai: 財務分析 -> 現金金流表
        """
        today_dict = self._get_today()

        today = today_dict['today']
        this_season = (today.month - 1) // 3 + 1
        start_date = "2014-01-01"
        end_date = today.strftime("%Y-%m-%d")

        query_data = self.query_seasonal_data(ticker,
                                              start_date=start_date,
                                              end_date=end_date,
                                              sheet='cash_flow',
                                              target_season=this_season)

        index_names = []

        return_dict = {
            "ticker": query_data[0]['ticker'],
            "company_name": query_data[0]['company_name'],
        }

        table_dict = dict()
        CASHO_dict = dict()  # 營業活動
        CASHI_dict = dict()  # 投資活動
        CASHF_dict = dict()  # 籌資活動

        this_season = query_data[-1]['seasonal_data']['season']

        checkpoints = ["營業活動之現金流量－間接法", "投資活動之現金流量", "籌資活動之現金流量"]
        main_cash_flows = [
            "營業活動之淨現金流入（流出）", "投資活動之淨現金流入（流出）", "籌資活動之淨現金流入（流出）"
        ]

        partial_cash_flows = [CASHO_dict, CASHI_dict, CASHF_dict]

        for data in query_data:
            year = data['seasonal_data']['year']
            season = data['seasonal_data']['season']

            time_index = f"{year}Q{season}"

            if (season == this_season):
                cash_flow = data['seasonal_data']['cash_flow']
                main_cash_flow_name = None
                partial_cash_flow = None
                next_checkpoint = 0

                for index_name, value in cash_flow.items():
                    if (next_checkpoint < 3
                            and index_name == checkpoints[next_checkpoint]):
                        main_cash_flow_name = main_cash_flows[next_checkpoint]
                        partial_cash_flow = partial_cash_flows[next_checkpoint]
                        next_checkpoint += 1
                    try:
                        table_dict[time_index][index_name]['value'] = value[
                            'value']
                        if (value['value']):
                            table_dict[time_index][index_name][
                                'percentage'] = value['value'] / cash_flow[
                                    main_cash_flow_name]['value']
                        else:
                            table_dict[time_index][index_name][
                                'percentage'] = None
                    except:
                        if (time_index not in table_dict.keys()):
                            table_dict[time_index] = dict()
                        table_dict[time_index][index_name] = dict()

                        table_dict[time_index][index_name]['value'] = value[
                            'value']
                        if (value['value']):
                            table_dict[time_index][index_name][
                                'percentage'] = value['value'] / cash_flow[
                                    main_cash_flow_name]['value']
                        else:
                            table_dict[time_index][index_name][
                                'percentage'] = None

                    try:
                        partial_cash_flow[time_index][index_name] = table_dict[
                            time_index][index_name]
                    except:
                        if (time_index not in partial_cash_flow.keys()):
                            partial_cash_flow[time_index] = dict()
                        partial_cash_flow[time_index][index_name] = table_dict[
                            time_index][index_name]

                index_names += list(cash_flow.keys())

        index_names = list(dict.fromkeys(index_names))

        cash_flow_table = pd.DataFrame(table_dict)
        cash_flow_table = self._expand_value_percentage(cash_flow_table)

        CASHO_table = pd.DataFrame(CASHO_dict)
        CASHO_table = self._expand_value_percentage(CASHO_table)

        CASHI_table = pd.DataFrame(CASHI_dict)
        CASHI_table = self._expand_value_percentage(CASHI_table)

        CASHF_table = pd.DataFrame(CASHF_dict)
        CASHF_table = self._expand_value_percentage(CASHF_table)

        return_dict['cash_flow'] = cash_flow_table
        return_dict['CASHO'] = CASHO_table
        return_dict['CASHI'] = CASHI_table
        return_dict['CASHF'] = CASHF_table

        return return_dict