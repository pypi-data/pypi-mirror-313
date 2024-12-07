import backtrader as bt
from ffquant.indicators.Trend import Trend
from ffquant.utils.Logger import stdout_log

__ALL__ = ['TrendAdjust']

class TrendAdjust(bt.Indicator):
    (BEARISH, NA, BULLISH) = (-1, 0, 1)

    params = (
        ('symbol', 'CAPITALCOM:HK50'),
        ('short_rsi_period', 3),
        ('long_rsi_period', 14),
        ('debug', False),
    )

    lines = ('trend_adj',)

    def __init__(self):
        super(TrendAdjust, self).__init__()
        self.addminperiod(self.p.long_rsi_period)

        self.trend = Trend(symbol=self.p.symbol, debug=False)

        self.fast_rsi = bt.indicators.RSI(self.data.close, period=self.p.short_rsi_period)
        self.slow_rsi = bt.indicators.RSI(self.data.close, period=self.p.long_rsi_period)
        self.crossover = bt.indicators.CrossOver(self.fast_rsi, self.slow_rsi)

        self.prev_diff = None

        self.trend_now = None
        self.trend_last = None

    def next(self):
        self.trend_now = self.trend[0]

        current_diff = self.fast_rsi[0] - self.slow_rsi[0]
        if self.trend_last is not None:

            if self.trend_now == TrendAdjust.BEARISH and self.crossover[0] == -1:
                if self.p.debug:
                    stdout_log(f"{self.__class__.__name__}, Changing to BEARISH when fast RSI downcrossing slow is now allowd, forcing it to BULLISH")
                self.trend_now = TrendAdjust.BULLISH
            elif self.trend_now == TrendAdjust.BEARISH \
                and self.prev_diff is not None \
                    and current_diff < self.prev_diff:
                if self.p.debug:
                    stdout_log(f"{self.__class__.__name__}, Changing to BEARISH when fast RSI approaching slow from above is now allowd, forcing it to BULLISH")
                self.trend_now = TrendAdjust.BULLISH
            elif self.trend_now == TrendAdjust.BULLISH and self.crossover[0] == 1:
                if self.p.debug:
                    stdout_log(f"{self.__class__.__name__}, Changing to BULLISH when fast RSI upcrossing slow is now allowd, forcing it to BEARISH")
                self.trend_now = TrendAdjust.BEARISH
            elif self.trend_now == TrendAdjust.BULLISH \
                and self.prev_diff is not None \
                        and current_diff > self.prev_diff:
                if self.p.debug:
                    stdout_log(f"{self.__class__.__name__}, Changing to BULLISH when fast RSI approaching slow from below is now allowd, forcing it to BEARISH")
                self.trend_now = TrendAdjust.BEARISH

        self.lines.trend_adj[0] = self.trend_now

        self.trend_last = self.trend_now
        self.prev_diff = current_diff