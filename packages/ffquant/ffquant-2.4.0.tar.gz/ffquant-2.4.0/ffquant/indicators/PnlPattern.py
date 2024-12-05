import backtrader as bt
import pytz
from ffquant.utils.Logger import stdout_log
import math

__ALL__ = ['PnlPattern']

class PnlPattern(bt.Indicator):
    (UNKNOWN, END_OF_DOWNTREND, DOWNTREND, CONSOLIDATION, UPTREND, END_OF_UPTREND) = (float('-inf'), -2, -1, 0, 1, 2)

    params = (
        ('long_period', 50),
        ('debug', False)
    )

    lines = ('pattern',)

    def __init__(self):
        super(PnlPattern, self).__init__()
        self.addminperiod(self.p.long_period)
        self.sma_long = bt.indicators.SimpleMovingAverage(self.data.close, period=self.p.long_period)
        self.cache = {}
        self.close_price = []
        self.portfolio_value = []
        self.short_portfolio_value_change_rate_list = []
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
            self.portfolio_value.append(self._owner.broker.getvalue())
            
            short_window = self.window_size_short
            if len(self.close_price) < self.window_size_short:
                short_window = len(self.close_price)
                
            # 这里是判断价格的
            short_portfolio_value_change_rate = (self.portfolio_value[-1] - self.portfolio_value[-short_window]) / self.portfolio_value[-short_window]
            self.short_portfolio_value_change_rate_list.append(short_portfolio_value_change_rate)
            
            # 获取近20根k线的最高价和最低价
            left_window_size = 21 if len(self.portfolio_value) >= 21 else len(self.portfolio_value)
            right_window_size = 1
            if right_window_size == left_window_size:
                highest_portfolio_value = self.portfolio_value[0]
                lowest_portfolio_value = self.portfolio_value[0]
            else:
                highest_portfolio_value = max(self.portfolio_value[-left_window_size:-right_window_size])
                lowest_portfolio_value = min(self.portfolio_value[-left_window_size:-right_window_size])
            
            # 用于判断当前行情
            self.cache[current_bar_time_str] = self.determine_pattern(self.data.open[0], self.data.high[0], self.data.low[0], self.data.close[0], self.portfolio_value[-1], self.sma_long, self.short_portfolio_value_change_rate_list[-5:], highest_portfolio_value, lowest_portfolio_value)
        else:
            if self.p.debug:
                stdout_log(f"{self.__class__.__name__}, current_time_str: {current_bar_time_str}, hit cache: {self.cache[current_bar_time_str]}")
        self.lines.pattern[0] = self.cache[current_bar_time_str]

    def determine_pattern(self, bar_open_price, bar_high_price, bar_low_price, bar_close_price, account_value, ema_50, account_value_rate_list, high_account_value_in_20, low_account_value_in_20):
        ret = self.lines.pattern[-1]
        if (ema_50 > bar_low_price) & (ema_50 < bar_high_price):
            ret = PnlPattern.CONSOLIDATION
        elif self.determine_trend(account_value_rate_list, self.count_up_trend(account_value_rate_list)) and account_value > high_account_value_in_20:
            ret = PnlPattern.UPTREND
        elif self.determine_trend(account_value_rate_list, self.count_down_trend(account_value_rate_list)) and account_value < low_account_value_in_20:
            ret = PnlPattern.DOWNTREND
        elif self.lines.pattern[-1] == PnlPattern.UPTREND \
            and not ((ema_50 > bar_low_price) & (ema_50 < bar_high_price)) \
                and not self.determine_trend(account_value_rate_list, self.count_up_trend(account_value_rate_list)) \
                    and not self.determine_trend(account_value_rate_list, self.count_down_trend(account_value_rate_list)):
            ret = PnlPattern.END_OF_UPTREND
        elif self.lines.pattern[-1] == PnlPattern.DOWNTREND \
            and not ((ema_50 > bar_low_price) & (ema_50 < bar_high_price)) \
                and not self.determine_trend(account_value_rate_list, self.count_up_trend(account_value_rate_list)) \
                    and not self.determine_trend(account_value_rate_list, self.count_down_trend(account_value_rate_list)):
            ret = PnlPattern.END_OF_DOWNTREND
        elif math.isnan(self.lines.pattern[-1]) or self.lines.pattern[-1] == PnlPattern.UNKNOWN:
            ret = PnlPattern.CONSOLIDATION
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
        if count / len(price_rate_list) >= 0.8:
            return True
        else:
            return False