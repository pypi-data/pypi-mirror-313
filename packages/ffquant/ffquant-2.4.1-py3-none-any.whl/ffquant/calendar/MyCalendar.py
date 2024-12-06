import os
from datetime import datetime
from ffquant.utils.Logger import stdout_log
import requests

__ALL__ = ['MyCalendar']

class MyCalendar:
    def __init__(self):
        self.base_url = f"{os.environ.get('FINTECHFF_CALENDAR_BASE_URL', 'http://192.168.25.98')}"
        pass

    """
    Checks if a given stock symbol is tradable at a specific date and time.

    Parameters:
        symbol (str): The stock symbol to check.
        dt (str): The date and time(Hong Kong timezone) to check. Format: 'YYYY-mm-dd HH:MM:SS'.

    Returns:
        bool: True if the symbol is tradable, False otherwise.
    """
    def isSymbolTradable(self, symbol: str, dt: str, debug = False) -> bool:
        broker = None
        if str(symbol).__contains__('@'):
            symbol, broker = symbol.split('@')

        url = "http://192.168.25.247:8220/current/trade/status"
        params = {
            "symbol": symbol,
            "time":dt
        }

        response = requests.get(url, params=params).json()
        if debug:
            stdout_log(f"MyCalendar, response: {response}, url: {url}, params: {params}")

        if response.get('code') == "200":
            return response['results']['isTradeOpen'] and response['results']['status'] == 'ACTIVE'
        else:
            return False


if __name__ == "__main__":
    calendar = MyCalendar()
    for hour in range(24):
        for minute in range(60):
            dt = f'2024-10-29 {hour:02d}:{minute:02d}:00'
            stdout_log(dt + ": " + ("Tradable" if calendar.isSymbolTradable('CAPITALCOM:HK50@tv', dt) else "Untradable"))