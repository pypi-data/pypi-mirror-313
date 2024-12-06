import backtrader as bt
from ffquant.utils.Logger import stdout_log
from datetime import datetime, timedelta
import pytz
import os
import requests
import time


__ALL__ = ['ThvAdjust']

class ThvAdjust(bt.Indicator):
    (BEARISH, NA, BULLISH) = (-1, 0, 1)
    params = (
        ('url', f"{os.environ.get('FINTECHFF_INDICATOR_BASE_URL', 'http://192.168.25.127:8288')}/index/list"),
        ('symbol', 'CAPITALCOM:HK50'),
        ('max_retries', 15),
        ('prefetch_size', 60),
        ('debug', False),
        ('test', False)
    )

    # cache the http response, because all indicators share the same response
    http_resp_cache = {}

    lines = ('thva',)

    def __init__(self):
        super(ThvAdjust, self).__init__()
        self.addminperiod(1)
        self.cache = {}

    def handle_api_resp(self, item):
        result_time_str = datetime.fromtimestamp(item['openTime']/ 1000).strftime('%Y-%m-%d %H:%M:%S')
        self.cache[result_time_str] = float('-inf')
        if item.get('data', None) is not None:
            v = item['data']
            if v == "-Infinity":
                v = float('-inf')
            self.cache[result_time_str] = v

        if self.p.debug:
            stdout_log(f"{self.__class__.__name__}, result_time_str: {result_time_str} {item.get('data', None)}")

    def determine_final_result(self):
        current_bar_time = self.data.datetime.datetime(0).replace(tzinfo=pytz.utc).astimezone()
        current_bar_time_str = current_bar_time.strftime('%Y-%m-%d %H:%M:%S')
        self.lines.thva[0] = self.cache[current_bar_time_str]

    def get_internal_key(self):
        key = f"indicator_trend_hold_adv_adjust"
        if self.p.test:
            key += "_test"
        return key

    def next(self):
        # skip the starting empty bars
        if len(self.data.close.array) == 0:
            return
        current_bar_time = self.data.datetime.datetime(0).replace(tzinfo=pytz.utc).astimezone()
        current_bar_time_str = current_bar_time.strftime('%Y-%m-%d %H:%M:%S')

        is_live = self.data.islive()
        if is_live:
            if current_bar_time_str not in self.cache:
                start_time = current_bar_time
                start_time_str = start_time.strftime('%Y-%m-%d %H:%M:%S')
                end_time = current_bar_time + timedelta(minutes=1)
                # make sure to fetch data up to latest minute
                now = datetime.now().replace(second=0, microsecond=0).astimezone()
                if end_time < now:
                    end_time = now
                end_time_str = end_time.strftime('%Y-%m-%d %H:%M:%S')

                params = self.prepare_params(start_time_str, end_time_str)

                # fill with -inf
                minutes_delta = int((end_time.timestamp() - start_time.timestamp()) / 60)
                for i in range(minutes_delta):
                    self.cache[(start_time + timedelta(minutes=i)).strftime('%Y-%m-%d %H:%M:%S')] = float('-inf')

                key = f"{self.p.symbol}_{start_time_str}_{end_time_str}"
                response = ThvAdjust.http_resp_cache.get(key, None)
                if response is None:
                    retry_count = 0
                    max_retry_count = self.p.max_retries
                    while retry_count < max_retry_count:
                        retry_count += 1
                        if self.p.debug:
                            stdout_log(f"{self.__class__.__name__}, fetch data params: {params}, url: {self.p.url}")

                        response = requests.get(self.p.url, params=params).json()
                        if self.p.debug:
                            stdout_log(f"{self.__class__.__name__}, fetch data response: {response}")

                        if response.get('code') != '200':
                            raise ValueError(f"{self.__class__.__name__}, API request failed: {response}")

                        ThvAdjust.http_resp_cache[key] = response
                        if response.get('results') is not None and len(response['results']) > 0:
                            results = response['results']
                            results.sort(key=lambda x: x['openTime'])
                            for result in results:
                                self.handle_api_resp(result)
                            break
                        time.sleep(1)
                else:
                    if response.get('results') is not None and len(response['results']) > 0:
                        results = response['results']
                        results.sort(key=lambda x: x['openTime'])
                        if results[len(results) - 1].get(self.get_internal_key(), None) is None:
                            if self.p.debug:
                                stdout_log(f"{self.__class__.__name__}, cached response's last result has no {self.get_internal_key()}, refresh data params: {params}, url: {self.p.url}")

                            time.sleep(1)
                            response = requests.get(self.p.url, params=params).json()
                            if self.p.debug:
                                stdout_log(f"{self.__class__.__name__}, refresh data response: {response}")

                            if response.get('code') != '200':
                                raise ValueError(f"{self.__class__.__name__}, API request failed: {response}")

                            ThvAdjust.http_resp_cache[key] = response
                            results = response['results']
                            results.sort(key=lambda x: x['openTime'])
                        else:
                            if self.p.debug:
                                stdout_log(f"{self.__class__.__name__}, use cached response: {response}")

                        for result in results:
                            self.handle_api_resp(result)
            else:
                if self.p.debug:
                    stdout_log(f"{self.__class__.__name__}, current_time_str: {current_bar_time_str}, hit cache: {self.cache[current_bar_time_str]}")
        else:
            if current_bar_time_str not in self.cache:
                start_time = current_bar_time
                start_time_str = start_time.strftime('%Y-%m-%d %H:%M:%S')
                end_time = current_bar_time + timedelta(minutes=self.p.prefetch_size)
                now = datetime.now().replace(second=0, microsecond=0).astimezone()
                if end_time > now:
                    end_time = now
                end_time_str = end_time.strftime('%Y-%m-%d %H:%M:%S')
                params = self.prepare_params(start_time_str, end_time_str)

                # fill with -inf value in this range
                for i in range(0, int((end_time.timestamp() - start_time.timestamp()) / 60)):
                    self.cache[(start_time + timedelta(minutes=i)).strftime('%Y-%m-%d %H:%M:%S')] = float('-inf')

                retry_count = 0
                max_retry_count = 1
                while retry_count < max_retry_count:
                    retry_count += 1
                    if self.p.debug:
                        stdout_log(f"{self.__class__.__name__}, fetch data params: {params}, url: {self.p.url}")

                    response = requests.get(self.p.url, params=params).json()
                    if self.p.debug:
                        stdout_log(f"{self.__class__.__name__}, fetch data response: {response}")

                    if response.get('code') != '200':
                        raise ValueError(f"{self.__class__.__name__}, API request failed: {response}")

                    if response.get('results') is not None and len(response['results']) > 0:
                        results = response['results']
                        results.sort(key=lambda x: x['openTime'])
                        for result in results:
                            self.handle_api_resp(result)
                        break
                    time.sleep(1)
            else:
                if self.p.debug:
                    stdout_log(f"{self.__class__.__name__}, current_time_str: {current_bar_time_str}, hit cache: {self.cache[current_bar_time_str]}")

        self.determine_final_result()

        # heartbeat info print
        for line_name in self.lines.getlinealiases():
            line = getattr(self.lines, line_name)
            if line[0] == float('-inf'):
                if len(self) > 1:
                    if self.p.debug:
                        stdout_log(f"{self.__class__.__name__}, {current_bar_time.astimezone().strftime('%Y-%m-%d %H:%M:%S')}, line[0] inherited from line[-1]: {line[-1]}")
                    line[0] = line[-1]
                else:
                    line[0] = 0

            stdout_log(f"[INFO], {self.__class__.__name__}, {current_bar_time.astimezone().strftime('%Y-%m-%d %H:%M:%S')}, {line_name}: {line[0]}")

    def prepare_params(self, start_time_str, end_time_str):
        params = {
            'type': self.get_internal_key(),
            'startTime' : start_time_str,
            'endTime' : end_time_str,
            'symbol' : self.p.symbol,
            'key_list': 'data'
        }

        return params