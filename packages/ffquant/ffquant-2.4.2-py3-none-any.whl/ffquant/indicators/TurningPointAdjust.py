import backtrader as bt
from ffquant.indicators.TurningPoint import TurningPoint
from ffquant.utils.Logger import stdout_log

__ALL__ = ['TurningPointAdjust']

class TurningPointAdjust(bt.Indicator):
    (DOWN, NA, UP) = (-1, 0, 1)

    params = (
        ('symbol', 'CAPITALCOM:HK50'),
        ('short_rsi_period', 3),
        ('long_rsi_period', 14),
        ('debug', False),
    )

    lines = ('tp_adj',)

    def __init__(self):
        super(TurningPointAdjust, self).__init__()
        self.addminperiod(self.p.long_rsi_period)

        self.tp = TurningPoint(symbol=self.p.symbol, debug=False)

        self.fast_rsi = bt.indicators.RSI(self.data.close, period=self.p.short_rsi_period)
        self.slow_rsi = bt.indicators.RSI(self.data.close, period=self.p.long_rsi_period)
        self.crossover = bt.indicators.CrossOver(self.fast_rsi, self.slow_rsi)

        self.prev_diff = None

        self.tp_now = None
        self.tp_last = None

    def next(self):
        self.tp_now = self.tp[0]

        current_diff = self.fast_rsi[0] - self.slow_rsi[0]
        if self.tp_last is not None:

            if self.tp_now == TurningPointAdjust.DOWN and self.crossover[0] == -1:
                if self.p.debug:
                    stdout_log(f"{self.__class__.__name__}, Changing to DOWN when fast RSI downcrossing slow is now allowd, forcing it to UP")
                self.tp_now = TurningPointAdjust.UP
            elif self.tp_now == TurningPointAdjust.DOWN \
                and self.prev_diff is not None \
                    and current_diff < self.prev_diff:
                if self.p.debug:
                    stdout_log(f"{self.__class__.__name__}, Changing to DOWN when fast RSI approaching slow from above is now allowd, forcing it to UP")
                self.tp_now = TurningPointAdjust.UP
            elif self.tp_now == TurningPointAdjust.UP and self.crossover[0] == 1:
                if self.p.debug:
                    stdout_log(f"{self.__class__.__name__}, Changing to UP when fast RSI upcrossing slow is now allowd, forcing it to DOWN")
                self.tp_now = TurningPointAdjust.DOWN
            elif self.tp_now == TurningPointAdjust.UP \
                and self.prev_diff is not None \
                        and current_diff > self.prev_diff:
                if self.p.debug:
                    stdout_log(f"{self.__class__.__name__}, Changing to UP when fast RSI approaching slow from below is now allowd, forcing it to DOWN")
                self.tp_now = TurningPointAdjust.DOWN

        self.lines.tp_adj[0] = self.tp_now

        self.tp_last = self.tp_now
        self.prev_diff = current_diff