from .base import StatsFetcher
import pandas as pd

class TechFetcher(StatsFetcher):
    
    def __init__(self, ticker:str, db_client):
        super().__init__(ticker, db_client)
        self.full_ohlcv = self._get_ohlcv()
        self.basic_indexes = ['SMA5', 'SMA20', 'SMA60', 'EMA5', 'EMA20', 
                              'EMA40', 'EMA12', 'EMA26', 'RSI7', 'RSI14',
                              'RSI21', 'MACD', 'Signal Line', 'Middle Band', 
                              'Upper Band', 'Lower Band', '%b', 'ATR', 
                              'BBW','EMA Cycle','EMA Cycle Instructions',
                              'Day Trading Signal']
        
        self.daily_index = TechProcessor.cal_basic_index(self.full_ohlcv)

        self.weekly_index = TechProcessor.resample(
            self.daily_index, 
            period= 'W',
            technical_indicators = self.basic_indexes
        )

        self.monthly_index = TechProcessor.resample(
            self.daily_index, 
            period= 'ME',
            technical_indicators = self.basic_indexes
        )

        self.quarterly_index = TechProcessor.resample(
            self.daily_index, 
            period= 'QE',
            technical_indicators = self.basic_indexes
        )

        self.yearly_index = TechProcessor.resample(
            self.daily_index, 
            period= 'YE',
            technical_indicators = self.basic_indexes
        )

    def _get_ohlcv(self):
        query = {'ticker': self.ticker}
        ticker_full = list(self.collection.find(query))

        if not ticker_full:
            raise ValueError(f"No data found for ticker: {self.ticker}")

        if 'daily_data' not in ticker_full[0] or ticker_full[0]['daily_data'] is None:
            raise KeyError("Missing 'daily_data' in the retrieved data")

        df = pd.DataFrame(ticker_full[0]['daily_data'])

        selected_cols = ['date','open','high','low','close','volume']

        return df[selected_cols]

    def get_daily(self):

        return self.daily_index

    def get_weekly(self):

        return self.weekly_index
    
    def get_monthly(self):

        return self.monthly_index

    def get_quarterly(self):

        return self.quarterly_index
    
    def get_yearly(self):

        return self.yearly_index

class TechProcessor:
    
    @staticmethod
    def cal_sma(closes: pd.Series, n_days: int) -> pd.Series:
        return closes.rolling(window=n_days).mean()

    @staticmethod
    def cal_ema(closes: pd.Series, n_days: int) -> pd.Series:
        return closes.ewm(span=n_days, adjust=False).mean()

    @staticmethod
    def cal_rsi(closes: pd.Series, n_days: int) -> pd.Series:
        delta = closes.diff(1)
        gain = (delta.where(delta > 0, 0)).rolling(window=n_days).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=n_days).mean()
        rs = gain / loss
        return 100 - (100 / (1 + rs))

    @staticmethod
    def cal_macd(ema12s: pd.Series, ema26s: pd.Series) -> pd.Series:
        return ema12s - ema26s

    @staticmethod
    def cal_single_line(macds: pd.Series, n_days: int = 9) -> pd.Series:
        return macds.ewm(span=n_days, adjust=False).mean()

    @staticmethod
    def cal_bollinger_bands(closes: pd.Series, n_days: int = 20) -> pd.DataFrame:
        middle = closes.rolling(window=n_days).mean()
        upper = middle + 2 * closes.rolling(window=n_days).std()
        lower = middle - 2 * closes.rolling(window=n_days).std()
        percent_b = (closes - lower) / (upper - lower)

        return pd.DataFrame(
            {
                'middle': middle,
                'upper': upper,
                "lower": lower,
                "%b": percent_b
            }
        )

    @staticmethod
    def cal_atr(highes: pd.Series, lows: pd.Series, closes: pd.Series, n_days: int) -> pd.Series:
        high_low = highes - lows
        high_close = (highes - closes.shift(1)).abs()
        low_close = (lows - closes.shift(1)).abs()

        true_range = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
        atr = true_range.rolling(window=n_days, min_periods=1).mean()

        return atr

    @staticmethod
    def check_tech_trend(ema5: float, ema20: float, ema40: float) -> str:
        if ema5 > ema20 > ema40:
            return '穩定上升期'
        elif ema20 > ema5 > ema40:
            return '牛市結束期'
        elif ema20 > ema40 > ema5:
            return '熊市入口期'
        elif ema40 > ema20 > ema5:
            return '穩定下跌期'
        elif ema40 > ema5 > ema20:
            return '熊市結束期'
        elif ema5 > ema40 > ema20:
            return '牛市入口期'
        else:
            return '未定義'

    @staticmethod
    def check_day_trading(
        close_today: float,
        close_yesterday: float,
        today_atr: float,
        today_rsi7: float,
        target_value=270,
        atr_thred=7.5
    ) -> str:
        reasons = []

        # 檢查規則 1: Close 今日 - Close 昨日
        if close_today - close_yesterday <= 0:
            reasons.append('今日收盤價未高於昨日收盤價')

        # 檢查規則 2: 今日 Close 是否大於目標值
        if close_today < target_value:
            reasons.append(f'今日收盤價未達到目標值{target_value}')

        # 檢查規則 3: ATR 是否大於 atr_thred
        if today_atr < atr_thred:
            reasons.append(f'ATR 值小於 {atr_thred}')

        # 檢查規則 4: RSI7 是否大於等於 40
        if today_rsi7 < 40:
            reasons.append('RSI7 值小於 40')

        # 根據檢查結果返回
        if not reasons:
            return '今日此股票為好的當沖標的'
        else:
            return f'今日此股票並非好的當沖標的, 原因: {", ".join(reasons)}'
    
    @staticmethod
    def cal_basic_index(ohlcvs:pd.DataFrame):
        
        # SMA
        ohlcvs['SMA5'] = TechProcessor.cal_sma(ohlcvs['close'], 5) 
        ohlcvs['SMA20'] = TechProcessor.cal_sma(ohlcvs['close'], 20)
        ohlcvs['SMA60'] = TechProcessor.cal_sma(ohlcvs['close'], 40)
            
        # EMA
        ohlcvs['EMA5'] = TechProcessor.cal_ema(ohlcvs['close'], 5)
        ohlcvs['EMA20'] = TechProcessor.cal_ema(ohlcvs['close'], 20)
        ohlcvs['EMA40'] = TechProcessor.cal_ema(ohlcvs['close'], 40)

        ohlcvs['EMA12'] = TechProcessor.cal_ema(ohlcvs['close'], 12)
        ohlcvs['EMA26'] = TechProcessor.cal_ema(ohlcvs['close'], 26)

        # RSI
        ohlcvs['RSI7'] = TechProcessor.cal_rsi(ohlcvs['close'], 7)
        ohlcvs['RSI14'] = TechProcessor.cal_rsi(ohlcvs['close'], 14)
        ohlcvs['RSI21'] = TechProcessor.cal_rsi(ohlcvs['close'], 21)

        # MACD
        ohlcvs['MACD'] = TechProcessor.cal_macd(ohlcvs['EMA12'], ohlcvs['EMA26'])
        ohlcvs['Signal Line'] = TechProcessor.cal_single_line(ohlcvs['MACD'], 9)
        
        # BANDS
        bands = TechProcessor.cal_bollinger_bands(ohlcvs['close'], 20)
        ohlcvs['Middle Band'] = bands['middle']
        ohlcvs['Upper Band'] = bands['upper']
        ohlcvs['Lower Band'] = bands['lower']
        ohlcvs['%b'] = bands['%b']
        ohlcvs['BBW'] = (ohlcvs["Upper Band"] - ohlcvs["Lower Band"]) / ohlcvs["Middle Band"]

        # ATR
        ohlcvs['ATR'] = TechProcessor.cal_atr(ohlcvs['high'],ohlcvs['low'],ohlcvs['close'],14)

        # EMA CYCLE
        ohlcvs['EMA Cycle'] = ohlcvs.apply(
            lambda row: TechProcessor.check_tech_trend(row['EMA5'], row['EMA20'], row['EMA40']),
            axis=1
        )
        guidance_map = {
            '穩定上升期': "三條移動平均線都左下右上, 買方優勢, 三線間隔越來越遠時, 進一步強攻",
            '牛市結束期': "ema20 & 40 左下右上, ema5 緩慢下滑, 行情仍強, 賣出條件為 ema5 持續下跌, ema20 停止上漲",
            '熊市入口期': "全數出清穩定上升期布局的多頭部位, 考慮提早佈局建立空頭部位",
            '穩定下跌期': "三條移動平均線都是左上右下, 賣方優勢, 三線間隔越來越遠時, 進一步強攻",
            '熊市結束期': "ema20 & 40 左上右下, ema5 緩慢上升, 行情仍走弱, 布局買進的條件是 ema 持續上漲, ema20 停止下降, 幾乎持平",
            '牛市入口期': "全數出清穩定下跌期布局的空頭部位, 考慮提早佈局多頭部位",
            '未定義': "無對應指導"
        }    

        ohlcvs['EMA Cycle Instructions'] = ohlcvs['EMA Cycle'].map(guidance_map)

        # DAY TRADE SELECTING
        ohlcvs['close_yesterday'] = ohlcvs['close'].shift(1)
        ohlcvs['Day Trading Signal'] = ohlcvs.apply(
            lambda row: TechProcessor.check_day_trading(
                close_today=row['close'],
                close_yesterday=row['close_yesterday'],  # 使用前一天的收盤價
                today_atr=row['ATR'],
                today_rsi7=row['RSI7']
            ),
            axis=1
        )

        return ohlcvs

    @staticmethod
    def resample(df: pd.DataFrame, period='W', technical_indicators=None, date_col='date'):
        """
        將 DataFrame 中的技術指標數據重新取樣為指定的時間週期。
        參數:
        df (pd.DataFrame): 包含技術指標的日線 DataFrame，必須包含 datetime 索引或指定的日期列。
        period (str): 重新取樣的時間週期，如 'W', 'ME', 'QE', 'YE'。
        technical_indicators (list): 需要重新取樣的技術指標列名。
        date_col (str): 包含日期的列名（如果不是索引）。
        
        返回:
        pd.DataFrame: 重新取樣後的 DataFrame。
        """
        # 標記輸入的日期是否是索引還是列
        original_index = df.index.name == date_col if df.index.name else False

        # 檢查是否需要將日期列設置為索引
        if not original_index and date_col in df.columns:
            df[date_col] = pd.to_datetime(df[date_col])
            df.set_index(date_col, inplace=True)

        # 過濾掉非數字型的列
        numeric_df = df.select_dtypes(include='number')

        # 預設的聚合方式
        agg_dict = {
            'open': 'first',
            'high': 'max',
            'low': 'min',
            'close': 'last',
            'volume': 'sum'
        }

        # 如果沒有提供 technical_indicators，設置默認技術指標
        if technical_indicators is None:
            technical_indicators = numeric_df.columns.tolist()

        # 將技術指標的聚合方式設置為 'mean'
        for indicator in technical_indicators:
            if indicator in numeric_df.columns:
                agg_dict[indicator] = 'mean'

        # 過濾出存在於 DataFrame 中的列
        existing_cols = {col: agg_dict[col] for col in agg_dict if col in numeric_df.columns}
        
        # 確保索引為 DatetimeIndex，進行重新取樣
        if not isinstance(df.index, pd.DatetimeIndex):
            raise TypeError("The DataFrame index must be a DatetimeIndex for resampling.")

        resampled_df = numeric_df.resample(period).agg(existing_cols)

        # 如果原始日期是列而非索引，將日期從索引還原為列並重置索引為範圍索引
        if not original_index:
            resampled_df.reset_index(inplace=True)

        return resampled_df


            

    


    