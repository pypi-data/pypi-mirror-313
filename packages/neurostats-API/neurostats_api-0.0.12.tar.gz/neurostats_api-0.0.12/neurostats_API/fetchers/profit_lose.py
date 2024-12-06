from .base import StatsFetcher, StatsDateTime
import importlib.resources as pkg_resources
import json
import numpy as np
import pandas as pd
from ..utils import StatsDateTime, StatsProcessor
import yaml



class ProfitLoseFetcher(StatsFetcher):
    """
    iFa.ai: 財務分析 -> 損益表
    """

    def __init__(self, ticker, db_client):
        super().__init__(ticker, db_client)

        self.table_settings = StatsProcessor.load_yaml("profit_lose.yaml")

    def prepare_query(self, target_season):
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
                "profit_loses": {
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
                                    "profit_lose":
                                    "$$target_season_data.profit_lose"
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

    def collect_data(self, target_season):
        pipeline = self.prepare_query(target_season)

        fetched_data = self.collection.aggregate(pipeline)

        return list(fetched_data)[-1]

    def query_data(self):
        try:
            latest_time = StatsDateTime.get_latest_time(
                self.ticker, self.collection)['last_update_time']
            target_season = latest_time['seasonal_data']['latest_season']
        except Exception as e:
            today = StatsDateTime.get_today()

            target_season = today.season
            target_season = target_season - 1 if target_season > 1 else 4

        fetched_data = self.collect_data(target_season)

        return self.process_data(fetched_data, target_season)

    def process_data(self, fetched_data, target_season):

        profit_loses = fetched_data['profit_loses']

        index_names = []

        table_dict = dict()
        grand_total_dict = dict()

        return_dict = {
            "ticker": fetched_data['ticker'],
            "company_name": fetched_data['company_name'],
        }

        for data in profit_loses:
            year = data['year']

            time_index = f"{year}Q{target_season}"

            # 蒐集整體的keys
            index_names += list(data['profit_lose'].keys())
            profit_lose = data['profit_lose']

            for index_name, value_dict in profit_lose.items():
                # (2020Q1, 項目, 金額或%)
                for item_name, item in value_dict.items():
                    if ('percentage' in item_name):
                        if (isinstance(item, (float, int))):
                            item = StatsProcessor.cal_non_percentage(item, to_str=True, postfix="%")
                    elif ('YoY' in item_name):
                        if (isinstance(item, (float, int))):
                            item = StatsProcessor.cal_percentage(item)
                    else:
                        if (isinstance(item, (float, int))):
                            item = StatsProcessor.cal_non_percentage(item,  postfix="千元")
                    try:
                        table_dict[index_name][(time_index, item_name)] = item

                    except KeyError:
                        if (index_name not in table_dict.keys()):
                            table_dict[index_name] = dict()
                            grand_total_dict[index_name] = dict()

                        table_dict[index_name][(time_index, item_name)] = item

        total_table = pd.DataFrame.from_dict(table_dict, orient='index')
        total_table.columns = pd.MultiIndex.from_tuples(total_table.columns)

        total_table = total_table.replace("N/A", None)

        for name, setting in self.table_settings.items():
            if ('target_index' in setting.keys()):
                target_indexes = [target.strip() for target in setting['target_index']]
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
