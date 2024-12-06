from .base import StatsFetcher
from datetime import datetime, timedelta
import json
import numpy as np
import pandas as pd
from ..utils import StatsDateTime, StatsProcessor
import importlib.resources as pkg_resources
import yaml


class MarginTradingFetcher(StatsFetcher):

    def __init__(self, ticker, db_client):
        """
        iFa -> 交易資訊 -> 資券變化

        包括: 
        1. 當日交易
        2. 一年內交易
        """
        super().__init__(ticker, db_client)

    def prepare_query(self, start_date, end_date):
        pipeline = super().prepare_query()

        pipeline.append({
            "$project": {
                "_id": 0,
                "ticker": 1,
                "company_name": 1,
                "daily_data": {
                    "$map": {
                        "input": {
                            "$filter": {
                                "input": "$daily_data",
                                "as": "daliy",
                                "cond": {
                                    "$and": [{
                                        "$gte": ["$$daliy.date", start_date]
                                    }, {
                                        "$lte": ["$$daliy.date", end_date]
                                    }]
                                }
                            }
                        },
                        "as": "target_daliy_data",
                        "in": "$$target_daliy_data"
                    }
                },
                "margin_trading": {
                    "$map": {
                        "input": {
                            "$filter": {
                                "input": "$margin_trading",
                                "as": "margin",
                                "cond": {
                                    "$and": [{
                                        "$gte": ["$$margin.date", start_date]
                                    }, {
                                        "$lte": ["$$margin.date", end_date]
                                    }]
                                }
                            }
                        },
                        "as": "target_margin_data",
                        "in": "$$target_margin_data"
                    }
                },
                "security_lending": {
                    "$map": {
                        "input": {
                            "$filter": {
                                "input": "$security_lending",
                                "as": "lending",
                                "cond": {
                                    "$and": [{
                                        "$gte": ["$$lending.date", start_date]
                                    }, {
                                        "$lte": ["$$lending.date", end_date]
                                    }]
                                }
                            }
                        },
                        "as": "target_lending_data",
                        "in": "$$target_lending_data"
                    }
                }
            }
        })

        return pipeline

    def collect_data(self, start_date, end_date):
        pipeline = self.prepare_query(start_date, end_date)

        fetched_data = self.collection.aggregate(pipeline).to_list()

        return fetched_data[-1]

    def query_data(self):
        try:
            latest_time = StatsDateTime.get_latest_time(
                self.ticker, self.collection)['last_update_time']
            latest_date = latest_time['margin_trading']['latest_date']
            end_date = latest_date.replace(hour=0,
                                           minute=0,
                                           second=0,
                                           microsecond=0)
        except Exception as e:
            print(
                f"No updated time for institution_trading in {self.ticker}, use current time instead"
            )
            end_date = datetime.now(self.timezone)
            end_date = end_date.replace(hour=0,
                                        minute=0,
                                        second=0,
                                        microsecond=0)

            if (end_date.hour < 22):  # 拿不到今天的資料
                end_date = end_date - timedelta(days=1)

        start_date = end_date - timedelta(days=365)

        fetched_data = self.collect_data(start_date, end_date)

        fetched_data['daily_data'] = sorted(fetched_data['daily_data'],
                                            key=lambda x: x['date'],
                                            reverse=True)
        fetched_data['margin_trading'] = sorted(fetched_data['margin_trading'],
                                                key=lambda x: x['date'],
                                                reverse=True)
        fetched_data['security_lending'] = sorted(
            fetched_data['security_lending'],
            key=lambda x: x['date'],
            reverse=True)

        table_dict = self.process_data(fetched_data)

        return table_dict

    def process_data(self, fetched_data):
        return_dict = dict()

        daily_datas = fetched_data['daily_data']
        latest_data = fetched_data['daily_data'][0]
        yesterday_data = fetched_data['daily_data'][1]

        # 交易價格與昨天交易
        price_dict = {
            "open": latest_data['open'],
            'close': latest_data['close'],
            'range': f"{latest_data['low']} - {latest_data['high']}",
            'volume': latest_data['volume'] / 1000,
            'last_open': yesterday_data['open'],
            'last_close': yesterday_data['close'],
            'last_range':
            f"{yesterday_data['low']} - {yesterday_data['high']}",
            'last_volume': yesterday_data['volume'] / 1000
        }
        annual_lows = [data['low'] for data in daily_datas]
        annual_highs = [data['high'] for data in daily_datas]
        lowest = np.min(annual_lows).item()
        highest = np.max(annual_highs).item()
        price_dict['52weeks_range'] = f"{lowest} - {highest}"

        return_dict['price'] = price_dict

        # 當日交易
        margin_trading = fetched_data['margin_trading']
        security_lending = fetched_data['security_lending']

        latest_margin_date = margin_trading[0]['date']
        latest_lending_date = security_lending[0]['date']
        ## 融資融券
        ### 先將所有現金償還與現券償還改成現償
        for trading in margin_trading:
            trading['financing']['現償'] = trading['financing'].pop('現金償還')
            trading['short_selling']['現償'] = trading['short_selling'].pop(
                '現券償還')
        ### 轉換
        latest_margin_trading = margin_trading[0]
        latest_margin_trading_df = {
            category: sub_dict
            for category, sub_dict in latest_margin_trading.items()
            if (isinstance(sub_dict, dict))
        }
        latest_margin_trading_df = pd.DataFrame.from_dict(
            latest_margin_trading_df)

        ## 借券表格
        latest_stock_lending = security_lending[0]['stock_lending']

        latest_stock_lending = {
            type_name: StatsProcessor.cal_round_int(value / 1000)
            for type_name, value in latest_stock_lending.items()
        }
        latest_stock_lending.pop("前日餘額")
        latest_stock_lending_df = pd.DataFrame.from_dict(latest_stock_lending,
                                                         orient="index",
                                                         columns=['stock_lending'])

        latest_dict = {
            "date": latest_margin_date,
            "margin_trading": latest_margin_trading_df,
            "stock_lending": latest_stock_lending_df,
            "security_offset": latest_margin_trading['資券互抵']
        }

        return_dict['latest_trading'] = latest_dict

        # 一年內
        annual_dates = [
            data['date'].strftime('%Y-%m-%d')
            for data in fetched_data['margin_trading']
        ]
        close_prices = {
            data['date'].strftime('%Y-%m-%d'): data['close']
            for data in fetched_data['daily_data']
            if data['date'].strftime('%Y-%m-%d') in annual_dates
        }
        volumes = {
            data['date'].strftime('%Y-%m-%d'):
            StatsProcessor.cal_round_int(data['volume'] / 1000)
            for data in fetched_data['daily_data']
            if data['date'].strftime('%Y-%m-%d') in annual_dates
        }

        ## 融資融券
        financings = {
            data['date'].strftime("%Y-%m-%d"): {
                f"融資_{type_name}": num_of_stocks
                for type_name, num_of_stocks in data['financing'].items()
            }
            for data in fetched_data['margin_trading']
        }

        short_sellings = {
            data['date'].strftime("%Y-%m-%d"): {
                f"融券_{type_name}": num_of_stocks
                for type_name, num_of_stocks in data['short_selling'].items()
            }
            for data in fetched_data['margin_trading']
        }

        ### 資券互抵
        security_offsets = {
            data['date'].strftime("%Y-%m-%d"): data['資券互抵']
            for data in fetched_data['margin_trading']
        }

        ## 借券(stock lendings)
        stock_lendings = {
            data['date'].strftime('%Y-%m-%d'): {
                f"借券_{type_name}":
                (num_of_stocks /
                 1000) if isinstance(num_of_stocks,
                                     (int, float)) else num_of_stocks
                for type_name, num_of_stocks in data['stock_lending'].items()
            }
            for data in fetched_data['security_lending']
        }

        annual_dict = {
            date: {
                "close": close_prices[date],
                "volume": volumes[date],
                **financings[date],
                **short_sellings[date],
                **stock_lendings[date], 
                "資券互抵":security_offsets[date]
            }
            for date in annual_dates
        }

        annual_table = pd.DataFrame.from_dict(annual_dict)

        return_dict['annual_margin'] = annual_table.T

        return return_dict
