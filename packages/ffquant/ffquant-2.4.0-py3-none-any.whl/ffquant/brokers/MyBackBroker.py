from backtrader.brokers import BackBroker
from backtrader.utils import AutoOrderedDict

__ALL__ = ['MyBackBroker']

class MyBackBroker(BackBroker):
    def __init__(self):
        super(MyBackBroker, self).__init__()

    

    def submit(self, order, check=True, **kwargs):
        o = super().submit(order, check)

        for key, value in kwargs.items():
            print(f"submit, {key}: {value}")

        pos_price = None
        pos_size = 0
        for pos in self.positions.values():
            pos_size = pos.size
            pos_price = pos.price

        info = AutoOrderedDict()
        info.symbol = order.data.p.symbol
        is_close_pos = kwargs.get('is_close_pos', False)
        if is_close_pos:
            info.is_close_pos = is_close_pos
            info.pos_price = pos_price
            info.pos_size = pos_size
        o.info = info

        return o
    
    def notify(self, order):
        info = order.info
        if info is not None:
            for key in info.keys():
                print(f"notify, {key}: {info[key]}")
            # print(f"notify, info: {info}")
        super().notify(order)