from ffquant.indicators.BaseIndicator import BaseIndicator
from datetime import datetime, timedelta
import pytz
from ffquant.utils.Logger import stdout_log

__ALL__ = ['Fluctuation']

class Fluctuation(BaseIndicator):
    (NA, ZHEN_DANG) = (0, 1)

    lines = ('fluct',)

    def __init__(self):
        super(Fluctuation, self).__init__()
        self.addminperiod(1)

    def handle_api_resp(self, item):
        internal_key = self.get_internal_key()
        result_time_str = datetime.fromtimestamp(item['openTime']/ 1000).strftime('%Y-%m-%d %H:%M:%S')
        if item.get(internal_key, None) is not None and item[internal_key] == 'ZHEN_DANG':
            self.cache[result_time_str] = self.ZHEN_DANG
        elif item.get(internal_key, None) is not None and item[internal_key] == 'NA':
            self.cache[result_time_str] = self.NA

        if self.p.debug:
            stdout_log(f"{self.__class__.__name__}, result_time_str: {result_time_str}, {internal_key}: {item.get(internal_key, None)}")

    def determine_final_result(self):
        current_bar_time = self.data.datetime.datetime(0).replace(tzinfo=pytz.utc).astimezone()
        current_bar_time_str = current_bar_time.strftime('%Y-%m-%d %H:%M:%S')
        self.lines.fluct[0] = self.cache[current_bar_time_str]

    def get_internal_key(self):
        return 'TYPE_ZHEN_DANG' if self.p.version is None else f'TYPE_ZHEN_DANG_{str(self.p.version).upper()}'