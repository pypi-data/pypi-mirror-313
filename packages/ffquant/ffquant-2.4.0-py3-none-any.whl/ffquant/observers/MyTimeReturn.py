import backtrader as bt
import pytz
import ffquant.utils.observer_data as observer_data

__ALL__ = ['MyTimeReturn']

class MyTimeReturn(bt.observers.TimeReturn):
    def __init__(self):
        super(MyTimeReturn, self).__init__()
        self.output_list = observer_data.treturn

    def start(self):
        super(MyTimeReturn, self).start()
        self.output_list.clear()

    def next(self):
        super(MyTimeReturn, self).next()
        msg = {
            "datetime": self.data.datetime.datetime(0).replace(tzinfo=pytz.utc).astimezone().strftime("%Y-%m-%d %H:%M:%S"),
            "timereturn": self.lines.timereturn[0]
        }
        self.output_list.append(msg)
