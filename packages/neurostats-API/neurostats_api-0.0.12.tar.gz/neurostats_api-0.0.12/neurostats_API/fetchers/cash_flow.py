from .base import StatsFetcher, StatsDateTime
import json
import numpy as np
import pandas as pd
from ..utils import StatsDateTime, StatsProcessor
import importlib.resources as pkg_resources
import yaml

class CashFlowFetcher(StatsFetcher):
    def __init__(self, ticker, db_client):
        super().__init__(ticker, db_client)

        self.cash_flow_dict = StatsProcessor.load_yaml(
            "cash_flow_percentage.yaml"
        )  # 計算子表格用
    
    def prepare_query(self, target_season):
        pipeline = super().prepare_query()

        pipeline.append({
            "$project": {
                "_id": 0,
                "ticker": 1,
                "company_name": 1,
                "cash_flows": {
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
                                    "cash_flow":
                                    "$$target_season_data.cash_flow"
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

        return list(fetched_data)[0]
    
    def query_data(self):
        
        try:
            latest_time = StatsDateTime.get_latest_time(self.ticker, self.collection)['last_update_time']
            target_season = latest_time['seasonal_data']['latest_season']
        
        except:
            today = StatsDateTime.get_today()
            target_season = today.season - 1 if (today.season > 1) else 4

        fetched_data = self.collect_data(target_season)

        return self.process_data(fetched_data, target_season)
    
    def process_data(self, fetched_data, target_season):
        """
        處理現金流量表頁面的所有表格
        金流表本身沒有比例 但是Ifa有算，
        項目所屬的情況也不一(分別所屬營業,投資,籌資三個活動)
        所以這裡選擇不用slicing處理
        """
        cash_flows = fetched_data['cash_flows']

        index_names = []
        column_names = []

        table_dict = dict()
        CASHO_dict = dict()
        CASHI_dict = dict()
        CASHF_dict = dict()

        return_dict = {
            "ticker": fetched_data['ticker'],
            "company_name": fetched_data['company_name'],
            "cash_flow": dict(),
            "CASHO": dict(),
            "CASHI": dict(),
            "CASHF": dict()
        }

        checkpoints = ["營業活動之現金流量－間接法", "投資活動之現金流量", "籌資活動之現金流量", "匯率變動對現金及約當現金之影響"]
        main_cash_flows = [
            "營業活動之淨現金流入（流出）", "投資活動之淨現金流入（流出）", "籌資活動之淨現金流入（流出）", None
        ] # 主要的比例對象
        partial_cash_flows = [CASHO_dict, CASHI_dict, CASHF_dict, dict()] 

        # 作法: dictionary中也有checkpoints，如果出現了就換下一個index去計算

        for data in cash_flows:
            year = data['year']

            time_index = f"{year}Q{target_season}"

            cash_flow = data['cash_flow']
            main_cash_flow_name = None
            partial_cash_flow = None
            next_checkpoint = 0

            for index_name, value in cash_flow.items():
                if (next_checkpoint < 3
                        and index_name == checkpoints[next_checkpoint]): # 找到了主要的變動點
                    main_cash_flow_name = main_cash_flows[next_checkpoint]
                    partial_cash_flow = partial_cash_flows[next_checkpoint]
                    next_checkpoint += 1
                try:
                    table_dict[time_index][index_name]['value'] = value[
                        'value']
                    if (value['value']):
                        ratio = np.round(
                                (value['value'] / cash_flow[
                                main_cash_flow_name]['value']) * 100, 2)
                        table_dict[time_index][index_name][
                            'percentage'] = f"{ratio}%"
                    else:
                        table_dict[time_index][index_name][
                            'percentage'] = None
                except: # 新增index再做一次
                    if (time_index not in table_dict.keys()):
                        table_dict[time_index] = dict()
                    table_dict[time_index][index_name] = dict()

                    table_dict[time_index][index_name]['value'] = value[
                        'value']
                    if (value['value']):
                        ratio = np.round(
                                (value['value'] / cash_flow[
                                main_cash_flow_name]['value']) * 100, 2) 
                        table_dict[time_index][index_name][
                            'percentage'] = f"{ratio}%"
                    else:
                        table_dict[time_index][index_name][
                            'percentage'] = None
                table_dict[time_index][index_name]['value'] = StatsProcessor.cal_non_percentage(value['value'], postfix="千元")
                try:
                    partial_cash_flow[time_index][index_name] = table_dict[
                        time_index][index_name]
                except:
                    if (time_index not in partial_cash_flow.keys()):
                        partial_cash_flow[time_index] = dict()
                    partial_cash_flow[time_index][index_name] = table_dict[
                        time_index][index_name]

            index_names += list(cash_flow.keys())

        # 轉成dictionary keys
        index_names = list(dict.fromkeys(index_names))

        cash_flow_table = pd.DataFrame(table_dict)
        cash_flow_table = StatsProcessor.expand_value_percentage(cash_flow_table)

        CASHO_table = pd.DataFrame(CASHO_dict)
        CASHO_table = StatsProcessor.expand_value_percentage(CASHO_table)

        CASHI_table = pd.DataFrame(CASHI_dict)
        CASHI_table = StatsProcessor.expand_value_percentage(CASHI_table)

        CASHF_table = pd.DataFrame(CASHF_dict)
        CASHF_table = StatsProcessor.expand_value_percentage(CASHF_table)

        return_dict['cash_flow'] = cash_flow_table
        return_dict['CASHO'] = CASHO_table
        return_dict['CASHI'] = CASHI_table
        return_dict['CASHF'] = CASHF_table

        return return_dict
