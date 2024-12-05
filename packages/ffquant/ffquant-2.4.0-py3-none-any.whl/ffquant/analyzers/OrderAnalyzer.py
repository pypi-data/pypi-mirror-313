import backtrader as bt
import pytz
import ffquant.utils.observer_data as observer_data

__ALL__ = ['OrderAnalyzer']

class OrderAnalyzer(bt.Analyzer):
    def __init__(self):
        self.order_infos = observer_data.order_info
    
    def start(self):
        super(OrderAnalyzer, self).start()
        self.order_infos.clear()

    def notify_order(self, order):
        if order.status == order.Completed:
            dt = self.data.datetime.datetime(0).replace(tzinfo=pytz.utc).astimezone().strftime("%Y-%m-%d %H:%M:%S")
            order_info = {
                'datetime': dt,
                'data': order,
                'position_after': self.strategy.position.size
            }
            self.order_infos.append(order_info)
    
    def get_analysis(self):
        return self.order_infos