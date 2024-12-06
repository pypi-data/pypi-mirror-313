import backtrader as bt
import threading
from ffquant.plot.dash_graph import show_perf_graph
from ffquant.observers.MyBkr import MyBkr
from ffquant.observers.MyBuySell import MyBuySell
from ffquant.observers.MyDrawDown import MyDrawDown
from ffquant.observers.MyTimeReturn import MyTimeReturn
from ffquant.analyzers.OrderAnalyzer import OrderAnalyzer
import inspect
import os
from ffquant.utils.dump_bt_data_utils import prepare_data_for_pickle
import time

__ALL__ = ['run_and_show_performance']

def run_and_show_performance(cerebro, strategy_name=None, riskfree_rate = 0.01, use_local_dash_url=False, debug=False):
    if hasattr(cerebro, 'runstrats'):
        raise Exception('Cerebro already run. Cannot run again')

    if strategy_name is None or strategy_name == '':
        frame = inspect.stack()[1]
        caller_file_path = frame.filename
        strategy_name = os.path.basename(caller_file_path)
        if strategy_name.endswith('.py'):
            strategy_name = strategy_name[:-3]

    add_observers(cerebro, debug)
    add_analyzers(cerebro, debug)

    is_live_trade = False
    for data in cerebro.datas:
        if data.islive():
            is_live_trade = True

    if is_live_trade:
        threading.Thread(target=lambda: cerebro.run(), daemon=True).start()
        time.sleep(15)
        backtest_data = prepare_data_for_pickle(strategy_name, riskfree_rate, use_local_dash_url, debug=debug)
        show_perf_graph(backtest_data, is_live=is_live_trade, debug=debug)
    else:
        cerebro.run()
        backtest_data = prepare_data_for_pickle(strategy_name, riskfree_rate, use_local_dash_url, debug=debug)
        show_perf_graph(backtest_data, is_live=is_live_trade, debug=debug)

def add_observers(cerebro, debug=False):
    cerebro.addobserver(MyBkr)
    cerebro.addobserver(MyBuySell)
    cerebro.addobserver(MyDrawDown)
    cerebro.addobserver(MyTimeReturn,
                        timeframe=bt.TimeFrame.Minutes, 
                        compression=1)

def add_analyzers(cerebro, debug=False):
    cerebro.addanalyzer(OrderAnalyzer)