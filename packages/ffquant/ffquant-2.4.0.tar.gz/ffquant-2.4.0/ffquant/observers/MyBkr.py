import backtrader as bt
import pytz
import ffquant.utils.observer_data as observer_data

__ALL__ = ['MyBkr']

class MyBkr(bt.observers.Broker):
    def __init__(self):
        super(MyBkr, self).__init__()
        self.output_list = observer_data.portfolio
        self.kline_output_list = observer_data.kline
        self.position_output_list = observer_data.position

    def start(self):
        super(MyBkr, self).start()
        self.output_list.clear()
        self.kline_output_list.clear()
        self.position_output_list.clear()

    def next(self):
        super(MyBkr, self).next()

        dt = self.data.datetime.datetime(0).replace(tzinfo=pytz.utc).astimezone().strftime("%Y-%m-%d %H:%M:%S")
        msg = {
            "datetime": dt,
            "portfolio": self.lines.value[0]
        }
        self.output_list.append(msg)

        self.kline_output_list.append({
            "datetime": dt,
            "open": self.data.open[0],
            "high": self.data.high[0],
            "low": self.data.low[0],
            "close": self.data.close[0]
        })

        self.position_output_list.append({
            "datetime": dt,
            "position": self._owner.position.size
        })
