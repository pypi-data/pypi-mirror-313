import backtrader as bt
import requests
import os
from datetime import datetime, timedelta, timezone
from ffquant.utils.Logger import stdout_log

__ALL__ = ['MyFeed']

class MyFeed(bt.feeds.DataBase):
    params = (
        ('volume', 'vol'),
        ('openinterest', None),
        ('url', f"{os.environ.get('FINTECHFF_FEED_BASE_URL', 'http://192.168.25.127:8288')}/symbol/info/list"),
        ('start_time', None),
        ('end_time', None),
        ('symbol', None),
        ('timeframe', bt.TimeFrame.Minutes),
        ('compression', 1),
        ('prefetch_size', 60),
        ('debug', False),
        ('backfill_size', 0),
    )

    lines = (('turnover'),)

    def __init__(self):
        if self.p.url is None or self.p.start_time is None or self.p.end_time is None or self.p.symbol is None:
            raise ValueError("Missing required parameters")

        self._timeframe = self.p.timeframe
        self._compression = self.p.compression
        super(MyFeed, self).__init__(fromdate=datetime.strptime(self.p.start_time, '%Y-%m-%d %H:%M:%S').replace(second=0, microsecond=0),
                                      todate=datetime.strptime(self.p.end_time, '%Y-%m-%d %H:%M:%S').replace(second=0, microsecond=0))
        self.cache = {}

    def _load(self):
        start_time = None
        if self.lines.datetime.idx == 0:
            # no datetime info is given for the first bar, so use the start_time in params as the start time.
            start_time = datetime.strptime(self.p.start_time, '%Y-%m-%d %H:%M:%S').replace(second=0, microsecond=0)
            if self.p.backfill_size > 0:
                start_time = start_time - timedelta(minutes=self.p.backfill_size)
        else:
            start_time = self.lines.datetime.datetime(-1).replace(tzinfo=timezone.utc).astimezone() + timedelta(minutes=1)

        end_time = start_time + timedelta(minutes=self.p.prefetch_size)
        start_time_str = start_time.strftime('%Y-%m-%d %H:%M:%S')
        end_time_str = end_time.strftime('%Y-%m-%d %H:%M:%S')

        if start_time.timestamp() >= datetime.strptime(self.p.end_time, '%Y-%m-%d %H:%M:%S').replace(second=0, microsecond=0).timestamp():
            return False

        key = f"{start_time_str}"
        if key not in self.cache:
            params = {
                'startTime': start_time_str,
                'endTime': end_time_str,
                'symbol': self.p.symbol
            }

            if self.p.debug:
                stdout_log(f"MyFeed, fetch data params: {params}")

            response = requests.get(self.p.url, params=params).json()
            if self.p.debug:
                stdout_log(f"MyFeed, fetch data response: {response}")

            if response.get('code') != '200':
                raise ValueError(f"MyFeed, API request failed: {response}")

            # fill with None value in this range
            for i in range(0, int((end_time.timestamp() - start_time.timestamp()) / 60)):
                self.cache[(start_time + timedelta(minutes=i)).strftime('%Y-%m-%d %H:%M:%S')] = None

            results = response.get('results', [])
            if results is not None:
                for result in results:
                    result_time_str = datetime.fromtimestamp(result['timeOpen'] / 1000.0, timezone.utc).astimezone().strftime('%Y-%m-%d %H:%M:%S')
                    self.cache[result_time_str] = result

        bar = self.cache.get(key, None)
        if bar is not None:
            self.lines.datetime[0] = bt.date2num(datetime.fromtimestamp(bar['timeOpen'] / 1000.0, timezone.utc))
            self.lines.open[0] = bar['open']
            self.lines.high[0] = bar['high']
            self.lines.low[0] = bar['low']
            self.lines.close[0] = bar['close']
            self.lines.volume[0] = bar['vol']
            self.lines.turnover[0] = bar['turnover']
            return True
        elif self.lines.datetime.idx > 0:
            # if there is no market data for current bar, use market data from last bar
            if self.p.debug:
                stdout_log(f"MyFeed, no market data for {start_time_str}, use last market data")
            self.lines.datetime[0] = bt.date2num(start_time.astimezone(timezone.utc))
            self.lines.open[0] = self.lines.close[-1]
            self.lines.high[0] = self.lines.close[-1]
            self.lines.low[0] = self.lines.close[-1]
            self.lines.close[0] = self.lines.close[-1]
            self.lines.volume[0] = 0.0
            self.lines.turnover[0] = 0.0
            return True
        else:
            backpeek_hours = 72
            params = {
                'startTime': (start_time - timedelta(hours=backpeek_hours)).strftime('%Y-%m-%d %H:%M:%S'),
                'endTime': start_time_str,
                'symbol': self.p.symbol
            }

            if self.p.debug:
                stdout_log(f"MyFeed, backpeek params: {params}")

            response = requests.get(self.p.url, params=params).json()
            if self.p.debug:
                stdout_log(f"MyFeed, backpeek response: {response}")

            if response.get('code') != '200':
                raise ValueError(f"MyFeed, API request failed: {response}")

            results = response.get('results', [])
            if results is not None and len(results) > 0:
                results.sort(key=lambda x: x['timeOpen'])
                result = results[len(results) - 1]
                result_time_str = datetime.fromtimestamp(result['timeOpen'] / 1000.0, timezone.utc).astimezone().strftime('%Y-%m-%d %H:%M:%S')
                if self.p.debug:
                    stdout_log(f"MyFeed, use close price {result['close']} from {result_time_str} to fill the starting bar")
                self.lines.datetime[0] = bt.date2num(start_time.astimezone(timezone.utc))
                self.lines.open[0] = result['close']
                self.lines.high[0] = result['close']
                self.lines.low[0] = result['close']
                self.lines.close[0] = result['close']
                self.lines.volume[0] = 0.0
                self.lines.turnover[0] = 0.0
                return True

            # failed to fetch data from backpeek requests. Fill will 0 values.
            self.lines.datetime[0] = bt.date2num(start_time.astimezone(timezone.utc))
            self.lines.open[0] = 0.0
            self.lines.high[0] = 0.0
            self.lines.low[0] = 0.0
            self.lines.close[0] = 0.0
            self.lines.volume[0] = 0.0
            self.lines.turnover[0] = 0.0
            return True
