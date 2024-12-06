import backtrader as bt
import pytz
import ffquant.utils.observer_data as observer_data
from backtrader.lineiterator import LineIterator

__ALL__ = ['MyBuySell']

class MyBuySell(bt.observers.BuySell):

    def __init__(self):
        super(MyBuySell, self).__init__()
        self.output_list = observer_data.buysell

    def start(self):
        super(MyBuySell, self).start()
        self.output_list.clear()

        strategy = self._owner
        for ind in strategy._lineiterators[LineIterator.IndType]:
            existing_cnt = 0
            for k, v in observer_data.ind_data.items():
                if k == ind.__class__.__name__ or k.startswith(f"{ind.__class__.__name__}-"):
                    existing_cnt += 1
            if existing_cnt > 0:
                observer_data.ind_data[f"{ind.__class__.__name__}-{existing_cnt + 1}"] = []
            else:
                observer_data.ind_data[ind.__class__.__name__] = []

    def next(self):
        super(MyBuySell, self).next()
        msg = {
            "datetime": self.data.datetime.datetime(0).replace(tzinfo=pytz.utc).astimezone().strftime("%Y-%m-%d %H:%M:%S"),
            "price": self.data.close[0],
            "buy": self.lines.buy[0],
            "sell": self.lines.sell[0]
        }
        self.output_list.append(msg)

        ind_cnt = {}
        strategy = self._owner
        for ind in strategy._lineiterators[LineIterator.IndType]:
            key = ind.__class__.__name__
            if ind_cnt.get(ind.__class__.__name__, 0) > 0:
                key = f"{ind.__class__.__name__}-{ind_cnt.get(ind.__class__.__name__, 0) + 1}"
            ind_cnt[ind.__class__.__name__] = ind_cnt.get(ind.__class__.__name__, 0) + 1

            history_values = observer_data.ind_data[key]
            history_values.append(ind[0])