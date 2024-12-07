import backtrader as bt
import pytz
import ffquant.utils.observer_data as observer_data

__ALL__ = ['MyDrawDown']

class MyDrawDown(bt.observers.DrawDown):
    def __init__(self):
        super(MyDrawDown, self).__init__()
        self.output_list = observer_data.drawdown

    def start(self):
        super(MyDrawDown, self).start()
        self.output_list.clear()

    def next(self):
        super(MyDrawDown, self).next()

        msg = {
            "datetime": self.data.datetime.datetime(0).replace(tzinfo=pytz.utc).astimezone().strftime("%Y-%m-%d %H:%M:%S"),
            "drawdown": self.lines.drawdown[0]
        }
        self.output_list.append(msg)
