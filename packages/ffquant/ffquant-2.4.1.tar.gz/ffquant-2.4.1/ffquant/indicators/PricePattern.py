import backtrader as bt
import pytz
from ffquant.utils.Logger import stdout_log
import math

__ALL__ = ['PricePattern']

class PricePattern(bt.Indicator):
    (UNKNOWN, END_OF_DOWNTREND, DOWNTREND, CONSOLIDATION, UPTREND, END_OF_UPTREND) = (float('-inf'), -2, -1, 0, 1, 2)

    params = (
        ('long_period', 50),
        ('debug', False)
    )

    lines = ('pattern',)

    def __init__(self):
        super(PricePattern, self).__init__()
        self.addminperiod(self.p.long_period)
        self.sma_long = bt.indicators.SimpleMovingAverage(self.data.close, period=self.p.long_period)
        self.cache = {}
        self.close_price = []
        self.short_price_change_rate_list = []
        self.window_size_short = 5

    def next(self):
        # skip the starting empty bars
        if len(self.data.close.array) == 0:
            return
        current_bar_time = self.data.datetime.datetime(0).replace(tzinfo=pytz.utc).astimezone()
        current_bar_time_str = current_bar_time.strftime('%Y-%m-%d %H:%M:%S')
        if current_bar_time_str not in self.cache:
            # 获取价格与成交量序列
            self.close_price.append(self.data.close[0])
            
            short_window = self.window_size_short
            if len(self.close_price) < self.window_size_short:
                short_window = len(self.close_price)
                
            # 这里是判断价格的
            if self.close_price[-short_window] != 0:
                short_price_change_rate = (self.close_price[-1] - self.close_price[-short_window]) / self.close_price[-short_window]
            else:
                short_price_change_rate = 0
            # short_price_change_rate = (self.close_price[-1] - self.close_price[-short_window]) / self.close_price[-short_window]
            self.short_price_change_rate_list.append(short_price_change_rate)
            
            # 获取近20根k线的最高价和最低价
            left_window_size = 21 if len(self.close_price) >= 21 else len(self.close_price)
            right_window_size = 1
            if right_window_size == left_window_size:
                highest_price = self.data.high[0]
                lowest_price = self.data.low[0]
            else:
                highest_price = max(self.close_price[-left_window_size:-right_window_size])
                lowest_price = min(self.close_price[-left_window_size:-right_window_size])
            
            # 用于判断当前行情
            self.cache[current_bar_time_str] = self.determine_pattern(self.data.open[0], self.data.high[0], self.data.low[0], self.data.close[0], self.sma_long, self.short_price_change_rate_list[-5:], highest_price, lowest_price,  self.close_price[-21:]) # close 用 21 是因为计算价格变化率会少一根
        else:
            if self.p.debug:
                stdout_log(f"{self.__class__.__name__}, current_time_str: {current_bar_time_str}, hit cache: {self.cache[current_bar_time_str]}")
        self.lines.pattern[0] = self.cache[current_bar_time_str]
    
    def judge_price_percent_rate(self, price_action, close_price_list):
        price_changes = []
        for i in range(1, len(close_price_list)):
            if close_price_list[i - 1] != 0:
                price_changes.append((close_price_list[i] - close_price_list[i - 1]) / close_price_list[i - 1] * 100)
            else:
                price_changes.append(0)
        # price_changes = [(close_price_list[i] - close_price_list[i - 1]) / close_price_list[i - 1] * 100 for i in range(1, len(close_price_list))]
        price_changes_slice = price_changes[-self.window_size_short:]
        
        if price_action == PricePattern.UPTREND or price_action == PricePattern.END_OF_UPTREND:
            count_below_neg_004 = sum(1 for change in price_changes if change <= -0.04)
            count_below_neg_005 = sum(1 for change in price_changes if change <= -0.05)
            if count_below_neg_004 >= 2 or count_below_neg_005 >= 1:
                return True
        elif price_action == PricePattern.DOWNTREND or price_action == PricePattern.END_OF_DOWNTREND:
            count_above_004 = sum(1 for change in price_changes if change >= 0.04)
            count_above_005 = sum(1 for change in price_changes if change >= 0.05)
            if count_above_004 >= 2 or count_above_005 >= 1:
                return True
        
        return False

    def determine_pattern(self, bar_open_price, bar_high_price, bar_low_price, bar_close_price, ema_50, price_rate_list, high_price_in_20, low_price_in_20, close_price_list):
        ret = self.lines.pattern[-1]
        if bar_open_price == 0:
            bar_rate = 0
        else:
            bar_rate = (bar_close_price - bar_open_price) / bar_open_price
            
        if (high_price_in_20 - low_price_in_20) == 0:
            high_low_rate = 0
        else:
            high_low_rate = (bar_close_price - low_price_in_20) / (high_price_in_20 - low_price_in_20)
        
        if bar_rate >= 0.01:
            ret = PricePattern.UNKNOWN
        # elif (self.lines.pattern[-1] == PricePattern.UPTREND or self.lines.pattern[-1] == PricePattern.END_OF_UPTREND) \
        #     and (high_low_rate >= 0.5) \
        #         and (self.judge_price_percent_rate(ret, close_price_list)):
        #     ret = PricePattern.DOWNTREND
        # elif (self.lines.pattern[-1] == PricePattern.DOWNTREND or self.lines.pattern[-1] == PricePattern.END_OF_DOWNTREND) \
        #     and (high_low_rate >= 0.5) \
        #         and (self.judge_price_percent_rate(ret, close_price_list)):
        #     ret = PricePattern.UPTREND
        elif (ema_50 > bar_low_price) & (ema_50 < bar_high_price):
            ret = PricePattern.CONSOLIDATION
        elif self.determine_trend(price_rate_list, self.count_up_trend(price_rate_list)) and bar_close_price > high_price_in_20:
            ret = PricePattern.UPTREND
        elif self.determine_trend(price_rate_list, self.count_down_trend(price_rate_list)) and bar_close_price < low_price_in_20:
            ret = PricePattern.DOWNTREND
        elif self.lines.pattern[-1] == PricePattern.UPTREND \
            and not ((ema_50 > bar_low_price) & (ema_50 < bar_high_price)) \
                and not self.determine_trend(price_rate_list, self.count_up_trend(price_rate_list)) \
                    and not self.determine_trend(price_rate_list, self.count_down_trend(price_rate_list)):
            ret = PricePattern.END_OF_UPTREND
        elif self.lines.pattern[-1] == PricePattern.DOWNTREND \
            and not ((ema_50 > bar_low_price) & (ema_50 < bar_high_price)) \
                and not self.determine_trend(price_rate_list, self.count_up_trend(price_rate_list)) \
                    and not self.determine_trend(price_rate_list, self.count_down_trend(price_rate_list)):
            ret = PricePattern.END_OF_DOWNTREND
        elif math.isnan(self.lines.pattern[-1]) or self.lines.pattern[-1] == PricePattern.UNKNOWN:
            ret = PricePattern.CONSOLIDATION
        return ret
        
    def count_up_trend(self, price_rate_list):
        count = 0
        for i in price_rate_list:
            if i > 0:
                count += 1
        return count
    
    def count_down_trend(self, price_rate_list):
        count = 0
        for i in price_rate_list:
            if i < 0:
                count += 1
        return count
    
    def determine_trend(self, price_rate_list, count):
        if not price_rate_list or len(price_rate_list) == 0:
            return False
        
        if count / len(price_rate_list) >= 0.8:
            return True
        else:
            return False