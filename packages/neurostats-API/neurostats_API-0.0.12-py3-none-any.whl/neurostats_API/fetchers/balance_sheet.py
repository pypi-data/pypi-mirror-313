from .base import StatsFetcher, StatsDateTime
import json
import numpy as np
import pandas as pd
from ..utils import StatsDateTime, StatsProcessor
import importlib.resources as pkg_resources
import yaml


class BalanceSheetFetcher(StatsFetcher):
    """
    對應iFa.ai -> 財務分析 ->  資產負債表
    """

    def __init__(self, ticker, db_client):
        super().__init__(ticker, db_client)
        self.table_settings = StatsProcessor.load_yaml("balance_sheet.yaml")

    def prepare_query(self, target_year, target_season):
        pipeline = super().prepare_query()

        target_query = {
            "year": "$$target_season_data.year",
            "season": "$$target_season_data.season",
            "balance_sheet": "$$$$target_season_data.balance_sheet"
        }

        pipeline.append({
            "$project": {
                "_id": 0,
                "ticker": 1,
                "company_name": 1,
                "balance_sheets": {
                    "$sortArray": {
                        "input": {
                            "$map": {
                                "input": {
                                    "$filter": {
                                        "input": "$seasonal_data",
                                        "as": "season",
                                        "cond": {
                                            "$eq":
                                            ["$$season.season", target_season]
                                        }
                                    }
                                },
                                "as": "target_season_data",
                                "in": {
                                    "year":
                                    "$$target_season_data.year",
                                    "season":
                                    "$$target_season_data.season",
                                    "balance_sheet":
                                    "$$target_season_data.balance_sheet"
                                }
                            }
                        },
                        "sortBy": {
                            "year": -1
                        }  # 按 year 降序排序
                    }
                }
            }
        })

        return pipeline

    def collect_data(self, target_year, target_season):
        pipeline = self.prepare_query(target_year, target_season)

        fetched_data = self.collection.aggregate(pipeline)

        fetched_data = list(fetched_data)

        return fetched_data[-1]

    def query_data(self):
        try:
            latest_time = StatsDateTime.get_latest_time(
                self.ticker, self.collection)['last_update_time']
            year = latest_time['seasonal_data']['latest_year']
            season = latest_time['seasonal_data']['latest_season']
        except Exception as e:
            today = StatsDateTime.get_today()
            year = today.year - 1 if (today.season == 1) else today.year
            season = 4 if (today.season == 1) else today.season - 1

        fetched_data = self.collect_data(year, season)

        return self.process_data(season, fetched_data)

    def process_data(self, target_season, fetched_data):
        return_dict = {
            "ticker": self.ticker,
            "company_name": fetched_data['company_name']
        }

        index_names = []

        table_dict = dict()

        balance_sheets = fetched_data['balance_sheets']

        # 將value與percentage跟著年分季度一筆筆取出
        for data in balance_sheets:
            year = data['year']

            time_index = f"{year}Q{target_season}"

            # 蒐集整體的keys
            index_names += list(data['balance_sheet'].keys())
            balance_sheet = data['balance_sheet']

            for index_name, value_dict in balance_sheet.items():
                for item_name, item in value_dict.items():
                    try:  # table_dict[項目][(2020Q1, '%')]
                        if (item_name == 'percentage'):
                            if (isinstance(item, (float, int))):
                                item = StatsProcessor.cal_non_percentage(item, to_str=True, postfix="%")
                        elif ("YoY" in item_name):
                            if (isinstance(item, (float, int))):
                                item = StatsProcessor.cal_percentage(item)
                        else:
                            if (isinstance(item, (float, int))):
                                item = StatsProcessor.cal_non_percentage(item,  postfix="千元")
                        table_dict[index_name][(time_index, item_name)] = item

                    except KeyError:
                        if (index_name not in table_dict.keys()):
                            table_dict[index_name] = dict()

                        table_dict[index_name][(time_index, item_name)] = item

        total_table = pd.DataFrame.from_dict(table_dict, orient='index')
        total_table.columns = pd.MultiIndex.from_tuples(total_table.columns)

        for name, setting in self.table_settings.items():
            if ('target_index' in setting.keys()):
                target_indexes = [target_index.strip() for target_index in setting['target_index']]
            else:
                target_indexes = [None]
            for target_index in target_indexes:
                try:
                    return_dict[name] = StatsProcessor.slice_multi_col_table(
                        total_table=total_table,
                        mode=setting['mode'],
                        target_index=target_index)
                    break
                except Exception as e:
                    continue
        return return_dict
