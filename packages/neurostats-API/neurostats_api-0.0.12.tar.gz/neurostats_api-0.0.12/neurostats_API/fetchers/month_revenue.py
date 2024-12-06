from .base import StatsFetcher, StatsDateTime
import json
import pandas as pd
from ..utils import StatsDateTime, StatsProcessor
import importlib.resources as pkg_resources
import yaml


class MonthRevenueFetcher(StatsFetcher):
    """
        iFa.ai: 財務分析 -> 每月營收
    """

    def __init__(self, ticker, db_client):
        super().__init__(ticker, db_client)

    def prepare_query(self, target_year, target_month):
        pipeline = super().prepare_query()

        pipeline.append({
            "$project": {
                "_id": 0,
                "ticker": 1,
                "company_name": 1,
                "monthly_data": {
                    "$sortArray": {
                        "input": "$monthly_data",
                        "sortBy": {
                            "year": -1,
                            "month": -1
                        }
                    }
                },
            }
        })

        return pipeline

    def collect_data(self, target_year, target_month):
        pipeline = self.prepare_query(target_year, target_month)

        fetched_data = self.collection.aggregate(pipeline)

        fetched_data = list(fetched_data)

        return fetched_data[-1]

    def query_data(self):
        try:
            latest_time = StatsDateTime.get_latest_time(
                self.ticker, self.collection)['last_update_time']
            target_year = latest_time['monthly_data']['latest_year']
            target_month = latest_time['monthly_data']['latest_month']
        except Exception as e:
            today = StatsDateTime.get_today()
            target_month = today.month
            target_year = today.year

        # Query data
        fetched_data = self.collect_data(target_year, target_month)

        return self.process_data(fetched_data)

    def process_data(self, fetched_data):

        monthly_data = fetched_data['monthly_data']
        for data in monthly_data:
            for key, value in data.items():
                if ("YoY" in key):
                    data[key] = StatsProcessor.cal_percentage(value)
                elif ("ratio" in key or 'percentage' in key):
                    data[key] = StatsProcessor.cal_non_percentage(value,
                                                                  to_str=True,
                                                                  postfix="%")
                elif (key not in ('year', 'month')):
                    data[key] = StatsProcessor.cal_non_percentage(value,
                                                                  postfix="千元")
        target_month = monthly_data[0]['month']
        monthly_df = pd.DataFrame(monthly_data)
        target_month_df = monthly_df[monthly_df['month'] == target_month]
        month_revenue_df = monthly_df.pivot(index='month',
                                            columns='year',
                                            values='revenue')

        grand_total_df = target_month_df.pivot(index='month',
                                               columns='year',
                                               values='grand_total')

        grand_total_df.rename(index={target_month: f"grand_total"},
                              inplace=True)
        month_revenue_df = month_revenue_df.sort_index(ascending=False)
        month_revenue_df = pd.concat([grand_total_df, month_revenue_df],
                                     axis=0)

        fetched_data['month_revenue'] = month_revenue_df[sorted(
            month_revenue_df.columns, reverse=True)]
        # 歷年月營收
        fetched_data[
            'this_month_revenue_over_years'] = target_month_df.set_index(
                "year")[[
                    "revenue", "revenue_increment_ratio", "YoY_1", "YoY_3",
                    "YoY_5", "YoY_10"
                ]].T
        # 歷年營收成長量
        fetched_data['grand_total_over_years'] = target_month_df.set_index(
            "year")[[
                "grand_total", "grand_total_increment_ratio",
                "grand_total_YoY_1", "grand_total_YoY_3", "grand_total_YoY_5",
                "grand_total_YoY_10"
            ]].T

        fetched_data.pop("monthly_data")

        return fetched_data
