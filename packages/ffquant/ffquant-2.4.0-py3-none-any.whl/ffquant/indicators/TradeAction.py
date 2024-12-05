from ffquant.indicators.BaseIndicator import BaseIndicator
from datetime import datetime, timedelta
import pytz
from ffquant.utils.Logger import stdout_log

__ALL__ = ['TradeAction']

class TradeAction(BaseIndicator):
    (BUY, NA, SELL) = (1, 0, -1)

    lines = ('ta',)

    def __init__(self):
        super(TradeAction, self).__init__()
        self.addminperiod(1)

    def handle_api_resp(self, item):
        internal_key = self.get_internal_key()
        result_time_str = datetime.fromtimestamp(item['openTime']/ 1000).strftime('%Y-%m-%d %H:%M:%S')
        if item.get(internal_key, None) is not None and item[internal_key] == 'BUY':
            self.cache[result_time_str] = self.BUY
        elif item.get(internal_key, None) is not None and item[internal_key] == 'SELL':
            self.cache[result_time_str] = self.SELL
        elif item.get(internal_key, None) is not None and item[internal_key] == 'NA':
            self.cache[result_time_str] = self.NA

        if self.p.debug:
            stdout_log(f"{self.__class__.__name__}, result_time_str: {result_time_str}, {internal_key}: {item.get(internal_key, None)}")

    def determine_final_result(self):
        current_bar_time = self.data.datetime.datetime(0).replace(tzinfo=pytz.utc).astimezone()
        current_bar_time_str = current_bar_time.strftime('%Y-%m-%d %H:%M:%S')
        self.lines.ta[0] = self.cache[current_bar_time_str]

    def get_internal_key(self):
        return 'TRADE_ACTION' if self.p.version is None else f'TRADE_ACTION_{str(self.p.version).upper()}'