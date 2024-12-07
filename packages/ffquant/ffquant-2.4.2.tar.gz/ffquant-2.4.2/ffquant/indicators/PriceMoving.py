from ffquant.indicators.BaseIndicator import BaseIndicator
from datetime import datetime, timedelta
import pytz
from ffquant.utils.Logger import stdout_log
import enum
import backtrader as bt

__ALL__ = ['PriceMoving']

CRASH_TNR_THRESHOLD = 0.6
RANGE_BOUND_TNR_THRESHOLD = 0.4
CRASH_PRICE_RATE_THRESHOLD = 0.0025


class Pattern(enum.Enum):
    NA = 0
    UP_V = 1
    DOWN_V = -1
    UP_FLAT = 2
    DOWN_FLAT = -2
    UP_CRASH = 3
    DOWN_CRASH = -3
    UNKNOWN = float('-inf')
    
    @staticmethod
    def from_value(value):
        for pattern in Pattern:
            if pattern.value == value:
                return pattern 
        return Pattern.UNKNOWN

class PriceMoving(bt.Indicator):
    lines = ('price_moving',)
    params = (
        ('window', 10),
        ('ratio', 0.6),
        ('debug', False),
    )

    def __init__(self):
        super(PriceMoving, self).__init__()
        self.addminperiod(self.params.window)
        self.window = self.params.window
        self.pattern_cache = Pattern.NA
        self.slice_index_cache = 0

    def next(self):
        # skip the starting empty bars
        if len(self.data.close.array) == 0:
            return
        current_bar_time = self.data.datetime.datetime(0).replace(tzinfo=pytz.utc).astimezone()
        current_bar_time_str = current_bar_time.strftime('%Y-%m-%d %H:%M:%S')
        tnr = self.calculate_tnr()
        if self.params.debug:
            stdout_log(f"{self.__class__.__name__}, current_time_str: {current_bar_time_str}, tnr: {tnr}")
        self.lines.price_moving[0] = tnr

    def calculate_tnr(self):
        if len(self.data.close) < 10:
            return Pattern.NA.value

        if self.pattern_cache == Pattern.UP_FLAT or self.pattern_cache == Pattern.DOWN_FLAT:
            self.window = self.window + 1
            if self.window > 13:
                self.window = self.params.window
                self.pattern_cache = Pattern.NA
                self.slice_index_cache = 0
        if len(self.data.close) >= self.window:
            size = self.window
        else:
            size = len(self.data.close)

        price_list = []
        for i in range(-size + 1, 1, 1):
            price_list.append(self.data.close[i])

        slice_index = int(size * self.params.ratio)
        if self.pattern_cache == Pattern.UP_FLAT or self.pattern_cache == Pattern.DOWN_FLAT:
            slice_index = self.slice_index_cache

        pre_price = price_list[:slice_index]
        cur_price = price_list[slice_index:]

        numerator_pre = abs(pre_price[-1] - pre_price[0])
        numerator_cur = abs(cur_price[-1] - cur_price[0])

        denominator_pre = sum(abs(pre_price[i] - pre_price[i - 1]) for i in range(1, len(pre_price)))
        denominator_cur = sum(abs(cur_price[i] - cur_price[i - 1]) for i in range(1, len(cur_price)))

        if denominator_cur == 0 or denominator_pre == 0:
            return Pattern.NA.value

        pre_tnr = numerator_pre / denominator_pre
        cur_tnr = numerator_cur / denominator_cur

        if not pre_price or not cur_price:
            return Pattern.NA.value

        if pre_price[0] > pre_price[-1]:
            pre_state = -1
        else:
            pre_state = 1

        if cur_price[0] > cur_price[-1]:
            cur_state = -1
        else:
            cur_state = 1
        bar_local_dt = self.data.datetime.datetime(0).replace(tzinfo=pytz.utc).astimezone()
        bar_local_dt_str = bar_local_dt.strftime('%Y-%m-%d %H:%M:%S')
        if self.params.debug:
            stdout_log(f"{self.__class__.__name__}, {bar_local_dt_str}, pre_tnr: {pre_tnr}, cur_tnr: {cur_tnr}, pre_state: {pre_state}, cur_state: {cur_state}")

        if cur_price[0] == 0 or pre_price[0] == 0:
            return Pattern.NA.value
        
        flag_pattern = Pattern.NA
        if pre_tnr > CRASH_TNR_THRESHOLD and cur_tnr > CRASH_TNR_THRESHOLD and pre_state == cur_state * -1 \
            and abs(cur_price[-1] - cur_price[0]) / cur_price[0] >= CRASH_PRICE_RATE_THRESHOLD \
                and abs(pre_price[-1] - pre_price[0]) / pre_price[0] >= CRASH_PRICE_RATE_THRESHOLD:
            if pre_state == 1 and cur_state == -1:
                flag_pattern = Pattern.UP_V
            elif pre_state == -1 and cur_state == 1:
                flag_pattern = Pattern.DOWN_V
        elif pre_tnr > CRASH_TNR_THRESHOLD and cur_tnr < RANGE_BOUND_TNR_THRESHOLD \
            and abs(pre_price[-1] - pre_price[0]) / pre_price[0] >= CRASH_PRICE_RATE_THRESHOLD:
                if pre_state == 1:
                    flag_pattern = Pattern.UP_FLAT
                elif pre_state == -1:
                    flag_pattern = Pattern.DOWN_FLAT
                self.pattern_cache = flag_pattern
                self.slice_index_cache = slice_index
        elif cur_tnr > CRASH_TNR_THRESHOLD \
            and abs(cur_price[-1] - cur_price[0]) / cur_price[0] >= CRASH_PRICE_RATE_THRESHOLD:
                if cur_state == 1:
                    flag_pattern = Pattern.UP_CRASH
                elif cur_state == -1:
                    flag_pattern = Pattern.DOWN_CRASH
        else:
            flag_pattern =  Pattern.NA

        return flag_pattern.value