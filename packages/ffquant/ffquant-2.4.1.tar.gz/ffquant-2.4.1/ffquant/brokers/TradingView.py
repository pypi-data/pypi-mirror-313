import requests
import os
import json
from ffquant.utils.Logger import stdout_log

__ALL__ = ['TradingView']

class TradingView:
    def __init__(self, id=None, debug=False):
        self.base_url = os.environ.get('TRADINGVIEW_BROKER_BASE_URL', 'http://192.168.25.90:3000/book')
        # test id: 14282761
        # production id: 14282759
        # production id: 14282760
        self.id = id if id is not None else os.environ.get('TRADINGVIEW_BROKER_ID', "14282761")
        self.debug = debug

    def _place_order(self, symbol="", type="", side="", qty=0):
        url = f"{self.base_url}?id={self.id}"
        data = {
            "symbol": symbol,
            "type": type,
            "side": side,
            "qty": float(qty)
        }
        payload = f"data={json.dumps(data)}"

        if self.debug:
            stdout_log(f"_place_order, payload: {payload}")

        headers = {
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        response = requests.post(url, headers=headers, data=payload).json()
        if self.debug:
            stdout_log(f"_place_order, response: {response}")
        return response

    def buy(self, symbol="", type="", qty=0):
        return self._place_order(symbol=symbol, type=type, side="buy", qty=qty)

    def sell(self, symbol="", type="", qty=0):
        return self._place_order(symbol=symbol, type=type, side="sell", qty=qty)