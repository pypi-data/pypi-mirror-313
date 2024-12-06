from .base import StatsFetcher
from datetime import datetime, timedelta
import json
import numpy as np
import pandas as pd
from ..utils import StatsDateTime, StatsProcessor
import importlib.resources as pkg_resources
import yaml


class InstitutionFetcher(StatsFetcher):
    """
    iFa -> 交易資訊 -> 法人買賣

    包括: 
    1. 當日交易
    2. 一年內交易
    """

    def __init__(self, ticker, db_client):
        super().__init__(ticker, db_client)

    def prepare_query(self, start_date, end_date):
        pipeline = super().prepare_query()

        # target_query = {
        #     "date": date,
        #     "institution_trading": "$$target_season_data.institution_trading"
        # }

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
                                "as": "daily",
                                "cond": {
                                    "$and": [{
                                        "$gte": ["$$daily.date", start_date]
                                    }, {
                                        "$lte": ["$$daily.date", end_date]
                                    }]
                                }
                            }
                        },
                        "as": "target_daily_data",
                        "in": "$$target_daily_data"
                    }
                },
                "institution_trading": {
                    "$map": {
                        "input": {
                            "$filter": {
                                "input": "$institution_trading",
                                "as": "institution",
                                "cond": {
                                    "$and": [{
                                        "$gte":
                                        ["$$institution.date", start_date]
                                    }, {
                                        "$lte":
                                        ["$$institution.date", end_date]
                                    }]
                                }
                            }
                        },
                        "as": "target_institution_data",
                        "in": "$$target_institution_data"
                    },
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
            latest_date = latest_time['institution_trading']['latest_date']
            end_date = latest_date.replace(hour=0,
                                           minute=0,
                                           second=0,
                                           microsecond=0)
        except Exception as e:
            print(
                f"No updated time for institution_trading in {self.ticker}, use current time instead"
            )
            end_date = datetime.now(self.timezone)
            end_date = date.replace(hour=0, minute=0, second=0, microsecond=0)

            if (date.hour < 17):  # 拿不到今天的資料
                end_date = end_date - timedelta(days=1)

        start_date = end_date - timedelta(days=365)

        fetched_data = self.collect_data(start_date, end_date)

        fetched_data['daily_data'] = sorted(fetched_data['daily_data'],
                                            key=lambda x: x['date'],
                                            reverse=True)
        fetched_data['institution_trading'] = sorted(
            fetched_data['institution_trading'],
            key=lambda x: x['date'],
            reverse=True)

        table_dict = self.process_data(fetched_data)

        return table_dict

    def process_data(self, fetched_data):
        table_dict = dict()

        daily_datas = fetched_data['daily_data']
        institution_tradings = fetched_data['institution_trading']

        latest_daily_data = daily_datas[0]
        yesterday_daily_data = daily_datas[1]

        # 交易價格與昨天交易
        price_dict = {
            "open": latest_daily_data['open'],
            'close': latest_daily_data['close'],
            'range':
            f"{latest_daily_data['low']} - {latest_daily_data['high']}",
            'volume': latest_daily_data['volume'] / 1000,
            'last_open': yesterday_daily_data['open'],
            'last_close': yesterday_daily_data['close'],
            'last_range':
            f"{yesterday_daily_data['low']} - {yesterday_daily_data['high']}",
            'last_volume': yesterday_daily_data['volume'] / 1000
        }
        # 一年範圍
        annual_lows = [data['low'] for data in daily_datas]
        annual_highs = [data['high'] for data in daily_datas]
        lowest = np.min(annual_lows).item()
        highest = np.max(annual_highs).item()

        price_dict['52weeks_range'] = f"{lowest} - {highest}"
        table_dict['price'] = price_dict

        # 發行股數 & 市值
        # 沒有實作

        # 今日法人買賣
        latest_trading = institution_tradings[0]
        table_dict['latest_trading'] = {
            "date":
            latest_trading['date'],
            "table":
            self.process_latest_trading(latest_trading,
                                        latest_daily_data['volume'])
        }
        # 一年內法人
        annual_dates = [data['date'].strftime("%Y-%m-%d") for data in daily_datas]
        annual_closes = {
            data['date'].strftime("%Y-%m-%d") : data['close']
            for data in daily_datas
            if (data['date'].strftime("%Y-%m-%d") in annual_dates)
        }
        annual_volumes = {
            data['date'].strftime("%Y-%m-%d") : data['volume']
            for data in daily_datas
            if (data['date'].strftime("%Y-%m-%d") in annual_dates)
        }
        annual_trading = {
            data['date'].strftime("%Y-%m-%d") : data
            for data in institution_tradings
        } 

        annual_trading = {
            date: {
                
                "close": annual_closes[date],
                "volume": annual_volumes[date],
                **annual_trading[date]
            }
            for date in annual_dates
        }

        table_dict['annual_trading'] = self.process_annual_trading(
            annual_dates, annual_trading)

        return table_dict

    def process_latest_trading(self, latest_trading, volume):
        latest_table = {
            "foreign": self.default_institution_chart(),
            "mutual": self.default_institution_chart(),
            "prop": self.default_institution_chart(),
            "institutional_investor": self.default_institution_chart(),
        }

        for key in latest_trading.keys():
            if (key.find("外陸資") >= 0 or key.find("外資") >= 0):
                self.target_institution(latest_trading,
                                        latest_table['foreign'], key, volume)
            elif (key.find("自營商") >= 0):
                self.target_institution(latest_trading, latest_table['prop'],
                                        key, volume)
            elif (key.find("投信") >= 0):
                self.target_institution(latest_trading, latest_table['mutual'],
                                        key, volume)
            elif (key.find("三大法人") >= 0):
                self.target_institution(latest_trading,
                                        latest_table['institutional_investor'],
                                        key, volume)

            for trade_type in ['buy', 'sell']:
                for unit in ['stock', 'percentage']:
                    latest_table['institutional_investor'][trade_type][
                        unit] = (latest_table['foreign'][trade_type][unit] +
                                 latest_table['prop'][trade_type][unit] +
                                 latest_table['mutual'][trade_type][unit])

        frames = []
        for category, trades in latest_table.items():
            temp_df = pd.DataFrame(trades).T
            temp_df['category'] = category
            frames.append(temp_df)

        latest_df = pd.concat(frames)
        latest_df = latest_df.reset_index().rename(columns={'index': 'type'})
        latest_df = latest_df[[
            'type', 'category', 'stock', 'price', 'average_price', 'percentage'
        ]]

        latest_df = pd.melt(latest_df,
                            id_vars=['type', 'category'],
                            var_name='variable',
                            value_name='value')

        latest_df = latest_df.pivot_table(index=['category', 'variable'],
                                          columns='type',
                                          values='value',
                                          aggfunc='first')

        # 重設列名，去除多層索引
        latest_df.columns.name = None  # 去除列名稱
        latest_df = latest_df.reset_index()

        return latest_df

    def process_annual_trading(self, dates, annual_tradings):
        return pd.DataFrame.from_dict(annual_tradings, orient='index')

    def target_institution(self, old_table, new_table, key, volume):
        if (key.find("買進") >= 0):
            self.cal_institution(old_table, new_table['buy'], key, volume)
        elif (key.find("賣出") >= 0):
            self.cal_institution(old_table, new_table['sell'], key, volume)
        elif (key.find("買賣超") >= 0):
            self.cal_institution(old_table, new_table['over_buy_sell'], key,
                                 volume)

    def cal_institution(self, old_table, new_table, key, volume):
        new_table['stock'] = np.round(old_table[key] / 1000, 2).item()
        new_table['percentage'] = np.round((old_table[key] / volume) * 100,
                                           2).item()

    def default_institution_chart(self):
        return {
            "buy": {
                "stock": 0,
                "price": 0,
                "average_price": 0,
                "percentage": 0
            },
            "sell": {
                "stock": 0,
                "price": 0,
                "average_price": 0,
                "percentage": 0
            },
            "over_buy_sell": {
                "stock": 0,
                "price": 0,
                "average_price": 0,
                "percentage": 0
            },
        }
