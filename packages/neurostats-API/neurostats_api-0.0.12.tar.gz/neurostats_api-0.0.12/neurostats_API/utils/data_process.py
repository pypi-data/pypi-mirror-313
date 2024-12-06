from importlib.resources import files
import json
import numpy as np
import pandas as pd
import yaml

target_metric_dict = {
    'value': ['value'],
    'value_and_percentage': ['value', 'percentage'],
    'percentage': ['percentage'],
    'grand_total': ['grand_total'],
    'grand_total_values': ['grand_total', 'grand_total_percentage'],
    'grand_total_percentage': ['grand_total_percentage'],
    'growth': [f'YoY_{i}' for i in [1, 3, 5, 10]],
    'grand_total_growth': [f"grand_total_YoY_{i}" for i in [1, 3, 5, 10]]
}


class StatsProcessor:
    """
    1. 讀檔: txt / yaml
    2. 將巢狀dictionary / DataFrame扁平化

    """

    @classmethod
    def load_txt(cls, filename, json_load=True):
        txt_path = files('neurostats_API.tools').joinpath(filename)
        with open(txt_path, 'r', encoding='utf-8') as f:
            data = json.load(f) if (json_load) else f.read()
        return data

    @classmethod
    def load_yaml(cls, filename):
        yaml_path = files('neurostats_API.tools').joinpath(filename)
        with open(yaml_path, 'r', encoding='utf-8') as f:
            data = yaml.safe_load(f)

        return data

    @classmethod
    def expand_value_percentage(cls, dataframe):

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

    @classmethod
    def slice_table(
            cls,
            total_table,
            mode='value',
            target_index=None,  # None or Str， 要特別抓哪個index
    ):
        """
        total_table: column應為 <時間>_<單位>
        對只有單層column的table，切出想要的index
        """
        times = [
            column.split("_")[0] for column in total_table.columns.unique()
        ]  #取出timeIndex
        try:
            target_metrics = target_metric_dict[mode]
        except KeyError as e:
            return f"mode Error: Get mode should be {list(target_metric_dict.keys())} but get {mode}"

        desired_order = [
            f"{time}_{value_name}" for time in times
            for value_name in target_metrics
        ]

        if (target_index):
            target_index = target_index.split()
            sliced_table = total_table.loc[target_index, desired_order].T

            return sliced_table.T

        else:
            return total_table.loc[:, desired_order]

    @classmethod
    def slice_multi_col_table(
            cls,
            total_table,
            mode='value',
            target_index=None,  # None or Str， 要特別抓哪個index
    ):
        """
        對Multicolumn的dataframe切出目標的index
        """
        times = total_table.columns.get_level_values(0).unique()
        try:
            target_metrics = target_metric_dict[mode]
        except KeyError as e:
            return f"mode Error: Get mode should be {list(target_metric_dict.keys())} but get {mode}"

        desired_order = [(time, value_name) for time in times
                         for value_name in target_metrics]

        if (target_index):
            target_index = target_index.split()
            sliced_table = total_table.loc[
                target_index, pd.IndexSlice[:,
                                            target_metrics]][desired_order].T
            if (mode == 'value_and_percentage'):  # 因應balance_sheet 頁面的格式
                return_table = sliced_table.T
                return_table.columns = [
                    "_".join(flatten_indexs)
                    for flatten_indexs in return_table.columns.to_flat_index()
                ]
                return return_table

            sliced_table = sliced_table.reset_index()
            sliced_table = sliced_table.pivot(index='level_1',
                                              columns='level_0',
                                              values=target_index).sort_index(
                                                  axis=1,
                                                  level=1,
                                                  ascending=False)

            sliced_table.columns = sliced_table.columns.get_level_values(1)
            sliced_table.columns.name = None
            sliced_table.index.name = None

            return sliced_table.reindex(target_metrics)

        else:
            return_table = total_table.loc[:, pd.IndexSlice[:,
                                                            target_metrics]][
                                                                desired_order]
            return_table.columns = [
                "_".join(flatten_indexs)
                for flatten_indexs in return_table.columns.to_flat_index()
            ]
            return return_table

    @classmethod
    def cal_percentage(cls, value, postfix="%"):
        if (isinstance(value, (float, int))):
            value = np.round(value * 100 , 2).item()
            value = f"{value:.2f}{postfix}"

            return value

        else:
            return value

    @classmethod
    def cal_non_percentage(cls, value, to_str=False, postfix="元"):
        if (isinstance(value, (float, int))):
            
            value = np.round(value, 2).item()
            if (postfix == "千元"):
                value *= 1000
                value = int(value)

                postfix = "元"

            if (to_str):
                if (isinstance(value, float)):
                    value = f"{value:.2f}{postfix}"
                    return value
                elif (isinstance(value, int)):
                    value = f"{value}{postfix}"
                    return value

            else:
                return value

        else:
            return value
    
    @classmethod
    def cal_round_int(cls, value):
        """
        將數值取到個位數後轉為int
        """
        if (isinstance(value, (int, float))):
            return int(np.round(value).item())
        else:
            return value
