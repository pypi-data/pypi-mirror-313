import backtrader as bt
from datetime import datetime
import os
import requests
import json
from backtrader.utils.py3 import queue
from backtrader.utils import AutoOrderedDict
import collections
from backtrader.position import Position
import getpass
from ffquant.utils.Logger import stdout_log
from urllib.parse import urlencode

__ALL__ = ['MyBroker']

class MyBroker(bt.BrokerBase):
    (TV_SIM1, TV_SIM2, TV_SIM3, TV_SIM4, TV_SIM5, FUTU_SIM1) = ("14078173", "14267474", "14267483", "15539511", "15539514", "9598674")

    def __init__(self, id=None, name="tv", debug=False, *args, **kwargs):
        super(MyBroker, self).__init__(*args, **kwargs)
        self.base_url = os.environ.get('MY_BROKER_BASE_URL', 'http://192.168.25.247:8220')
        self.id = id
        self.name = name
        self.cash = None
        self.value = None
        self.orders = {}
        self.pending_orders = list()
        self.notifs = queue.Queue()
        self.debug = debug
        self.positions = collections.defaultdict(Position)
        self.MIN_UPDATE_INTERVAL_SECONDS = 10
        self.last_cash_update_ts = 0
        self.last_value_update_ts = 0
        self.last_order_update_ts = 0
        self.last_position_update_ts = 0

    def getcash(self):
        if self.cash is None:
            self._update_cashvalue()
        return self.cash

    def getvalue(self, datas=None):
        if self.value is None:
            self._update_cashvalue()
        return self.value

    def getposition(self, data=None, symbol=None):
        position = bt.Position()

        target_symbol = data.p.symbol if data is not None else symbol
        if not self.positions.__contains__(target_symbol):
            self._update_positions()

        if self.positions.__contains__(target_symbol):
            position = self.positions[target_symbol]

        if self.debug:
            stdout_log(f"{self.__class__.__name__}, getposition, position size: {position.size}, price: {position.price}")

        return position

    def cancel(self, order):
        order_id = order.ref
        url = self.base_url + f"/cancel/order/{self.name}/{self.id}"
        data = {
            "tradeId": order_id,
        }
        payload = urlencode({"content": json.dumps(data)})
        if self.debug:
            stdout_log(f"{self.__class__.__name__}, cancel, payload: {payload}")

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        response = requests.post(url, headers=headers, data=payload).json()
        if self.debug:
            stdout_log(f"{self.__class__.__name__}, cancel, response: {response}")

        ret = True
        code = response['code']
        if code != '200':
            stdout_log(f"[CRITICAL], {self.__class__.__name__}, cancel failed, url: {url}, payload: {payload}, response: {response}")
            ret = False
        return ret

    def get_pending_orders(self):
        return self.pending_orders

    def get_orders_open(self):
        return self.get_pending_orders()

    def submit(self, order, **kwargs):
        url = self.base_url + f"/place/order/{self.name}/{self.id}"

        side = None
        if order.ordtype == bt.Order.Buy:
            if kwargs.get('is_close_pos', False):
                side = 'close'
            else:
                side = 'long'
        elif order.ordtype == bt.Order.Sell:
            if kwargs.get('is_close_pos', False):
                side = 'cover'
            else:
                side = 'short'

        order.size = abs(order.size)
        username = getpass.getuser()
        username = username[8:] if username.startswith('jupyter-') else username

        msg = ""
        if kwargs.get('is_tp', False):
            msg = "tp"
        elif kwargs.get('is_sl', False):
            msg = "sl"

        if kwargs.get("message", None) is not None:
            msg = ((msg + ":") if msg != "" else "") + kwargs.get("message")

        data = {
            "symbol": order.data.p.symbol,
            "side": side,
            "qty": order.size,
            "price": order.price,
            "type": "market" if order.exectype == bt.Order.Market else "limit",
            "username": username,
            "message": msg
        }
        payload = urlencode({"content": json.dumps(data)})
        if self.debug:
            stdout_log(f"{self.__class__.__name__}, submit, payload: {payload}")

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        response = requests.post(url, headers=headers, data=payload).json()
        if self.debug:
            stdout_log(f"{self.__class__.__name__}, submit, response: {response}")

        order_id = None
        if response.get('code') == "200":
            order_id = response['results']
            order.status = bt.Order.Submitted
            order.ref = order_id
            order.addinfo(**kwargs)

            self.orders[order_id] = order
        else:
            stdout_log(f"[CRITICAL], {self.__class__.__name__}, submit failed, url: {url}, payload: {payload}, response: {response}")

        return order

    def buy(self, owner, data, size, price=None, plimit=None, exectype=None, valid=None, tradeid=0, oco=None, trailamount=None, trailpercent=None, **kwargs):
        order = bt.order.BuyOrder(owner=owner, data=data, size=size, price=price, pricelimit=plimit, exectype=exectype, valid=valid, tradeid=tradeid, oco=oco, trailamount=trailamount, trailpercent=trailpercent)
        return self.submit(order, **kwargs)

    def sell(self, owner, data, size, price=None, plimit=None, exectype=None, valid=None, tradeid=0, oco=None, trailamount=None, trailpercent=None, **kwargs):
        order = bt.order.SellOrder(owner=owner, data=data, size=size, price=price, pricelimit=plimit, exectype=exectype, valid=valid, tradeid=tradeid, oco=oco, trailamount=trailamount, trailpercent=trailpercent)
        return self.submit(order, **kwargs)
    
    def get_notification(self):
        notif = None
        try:
            notif = self.notifs.get(False)
        except queue.Empty:
            pass

        return notif

    def next(self):
        if datetime.now().timestamp() - self.last_order_update_ts > self.MIN_UPDATE_INTERVAL_SECONDS:
            self.last_order_update_ts = datetime.now().timestamp()

            # Update order status
            trade_ids = []
            for order_id, order in self.orders.items():
                if order.status != bt.Order.Completed and order.status != bt.Order.Cancelled:
                    trade_ids.append(order_id)
            if len(trade_ids) > 0:
                url = self.base_url + f"/orders/query/{self.name}/{self.id}"
                data = {
                    "tradeIdList": trade_ids
                }
                payload = urlencode({"content": json.dumps(data)})

                if self.debug:
                    stdout_log(f"{self.__class__.__name__}, next, order query payload: {payload}")

                headers = {
                    'Content-Type': 'application/x-www-form-urlencoded'
                }

                response = requests.post(url, headers=headers, data=payload).json()
                if self.debug:
                    stdout_log(f"{self.__class__.__name__}, next, order query response: {response}")
                if response.get('code') == "200":
                    for item in response['results']:
                        item_status = None
                        if item['orderStatus'] == "pending" or item['orderStatus'] == "working":
                            item_status = bt.Order.Submitted
                        elif item['orderStatus'] == "cancelled":
                            item_status = bt.Order.Cancelled
                        elif item['orderStatus'] == "filled":
                            item_status = bt.Order.Completed
                        elif item['orderStatus'] == "rejected":
                            item_status = bt.Order.Rejected

                        order = self.orders.get(item['tradeId'], None)
                        if order is not None and order.status != item_status:
                            if self.debug:
                                stdout_log(f"{self.__class__.__name__}, next, order status changed, orderId: {order.ref}, old status: {order.getstatusname()}, new status: {bt.Order.Status[item_status]}")

                            if item_status == bt.Order.Completed:
                                order.executed.size = item['qty']
                                order.executed.price = item['executePrice']

                            order.status = item_status
                            self.orders[item['tradeId']] = order
                            self.notifs.put(order.clone())
                else:
                    stdout_log(f"[CRITICAL], {self.__class__.__name__}, order query failed, url: {url}, payload: {payload}, response: {response}")

            # Update pending orders
            url = self.base_url + f"/orders/query/{self.name}/{self.id}"
            data = {
                "orderStatusList": ["pending", "working"]
            }
            payload = urlencode({"content": json.dumps(data)})
            if self.debug:
                stdout_log(f"{self.__class__.__name__}, next, order query payload: {payload}")
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded'
            }
            response = requests.post(url, headers=headers, data=payload).json()
            if self.debug:
                stdout_log(f"{self.__class__.__name__}, next, order query response: {response}")
            if response.get('code') == "200":
                self.pending_orders.clear()
                for item in response['results']:
                    order_id = item['tradeId']
                    exec_type = bt.Order.Market
                    if item['tradeType'] == "limit":
                        exec_type = bt.Order.Limit

                    p_order = None
                    if item['tradeSide'] == 'buy':
                        p_order = bt.order.BuyOrder(owner=None,
                                                    data=None,
                                                    size=item['qty'],
                                                    price=item['allocationPrice'],
                                                    pricelimit=item['allocationPrice'],
                                                    exectype=exec_type,
                                                    valid=None,
                                                    tradeid=0,
                                                    oco=None,
                                                    trailamount=None,
                                                    trailpercent=None,
                                                    simulated=True)
                    else:
                        p_order = bt.order.SellOrder(owner=None,
                                                    data=None,
                                                    size=item['qty'],
                                                    price=item['allocationPrice'],
                                                    pricelimit=item['allocationPrice'],
                                                    exectype=exec_type,
                                                    valid=None,
                                                    tradeid=0,
                                                    oco=None,
                                                    trailamount=None,
                                                    trailpercent=None,
                                                    simulated=True)
                    p_order.p.simulated = False
                    p_order.ref = order_id
                    p_order.status = bt.Order.Submitted
                    self.pending_orders.append(p_order)
            else:
                stdout_log(f"[CRITICAL], {self.__class__.__name__}, order query failed, url: {url}, payload: {payload}, response: {response}")

        # Update positions
        self._update_positions()

        # Update cash & value
        self._update_cashvalue()

    def get_order(self, order_id):
        return self.orders.get(order_id, None)

    def _update_cashvalue(self):
        # cash
        if datetime.now().timestamp() - self.last_cash_update_ts > self.MIN_UPDATE_INTERVAL_SECONDS:
            self.last_cash_update_ts = datetime.now().timestamp()
            url = self.base_url + f"/balance/{self.name}/{self.id}"
            response = requests.get(url).json()
            if self.debug:
                stdout_log(f"{self.__class__.__name__}, _update_cashvalue, balance response: {response}")
            if response.get('code') == "200" and response['results'] is not None:
                self.cash = response['results']['balance']
            else:
                stdout_log(f"[CRITICAL], {self.__class__.__name__}, balance query failed, url: {url}, response: {response}")

        # value
        if self.cash is not None:
            if datetime.now().timestamp() - self.last_value_update_ts > self.MIN_UPDATE_INTERVAL_SECONDS:
                self.last_value_update_ts = datetime.now().timestamp()

                value = self.cash
                url = self.base_url + f"/positions/{self.name}/{self.id}"
                response = requests.get(url).json()
                if self.debug:
                    stdout_log(f"{self.__class__.__name__}, _update_cashvalue, positions response: {response}")
                if response.get('code') == "200":
                    for pos in response['results']:
                        if pos['qty'] == 0:
                            continue
                        if pos['tradeSide'] == 'buy':
                            value = value + pos['qty'] * (pos['latestPrice'] - pos['avgPrice'])
                        elif pos['tradeSide'] == 'sell':
                            value = value + pos['qty'] * (pos['avgPrice'] - pos['latestPrice'])
                else:
                    stdout_log(f"[CRITICAL], {self.__class__.__name__}, positions query failed, url: {url}, response: {response}")
                self.value = value

    def _update_positions(self):
        if datetime.now().timestamp() - self.last_position_update_ts > self.MIN_UPDATE_INTERVAL_SECONDS:
            self.last_position_update_ts = datetime.now().timestamp()

            if self.positions.__len__() > 0:
                self.positions.clear()

            url = self.base_url + f"/positions/{self.name}/{self.id}"
            response = requests.get(url).json()

            if self.debug:
                stdout_log(f"{self.__class__.__name__}, _update_positions, positions response: {response}")

            if response.get('code') == "200":
                for pos in response['results']:
                    if pos['qty'] != 0:
                        self.positions[pos['symbol']] = bt.Position(size=pos['qty'] if pos['tradeSide'] == 'buy' else -pos['qty'], price=pos['avgPrice'])
            else:
                stdout_log(f"[CRITICAL], {self.__class__.__name__}, positions query failed, url: {url}, response: {response}")