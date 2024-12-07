import os
import pickle
import backtrader as bt
from ffquant.utils.Logger import stdout_log
from pathlib import Path
import ffquant.utils.observer_data as observer_data

def wash_order_info(order_info, pickle_dict):
    order_list = list()
    for item in order_info:
        tmp_order_dict = dict()
        tmp_order_dict['datetime'] = item['datetime']
        tmp_order_dict['exec_type'] = "Market" if item['data'].exectype == bt.Order.Market else "Limit"
        tmp_order_dict['order_type'] = "Buy" if item['data'].ordtype == bt.Order.Buy else "Sell"
        tmp_order_dict['execute_price'] = item['data'].executed.price
        tmp_order_dict['execute_size'] = abs(item['data'].executed.size)
        tmp_order_dict['position_after'] = item['position_after']
        tmp_order_dict['origin'] = item['data'].info["origin"] if item['data'].info["origin"] is not None and not isinstance(item['data'].info["origin"], dict) else "Unknown"
        tmp_order_dict['message'] = item['data'].info["message"] if item['data'].info["message"] is not None and not isinstance(item['data'].info["message"], dict) else None
        order_list.append(tmp_order_dict)
    
    pickle_dict['order_info'] = order_list
    return pickle_dict

def prepare_data_for_pickle(strategy_name, riskfree_rate=0.01, use_local_dash_url=False, version="1.0.0", debug=False):
    pickle_dict = {}
    pickle_dict["version"] = version
    pickle_dict["strategy_name"] = strategy_name
    pickle_dict["use_local_dash_url"] = use_local_dash_url
    pickle_dict["riskfree_rate"] = riskfree_rate
    pickle_dict['treturn'] = observer_data.treturn
    pickle_dict['portfolio'] = observer_data.portfolio
    pickle_dict['buysell'] = observer_data.buysell
    pickle_dict['drawdown'] = observer_data.drawdown
    pickle_dict['kline'] = observer_data.kline
    pickle_dict['position'] = observer_data.position
    pickle_dict['ind_data'] = observer_data.ind_data

    # repack order info because it is not serializable
    pickle_dict = wash_order_info(observer_data.order_info, pickle_dict)

    return pickle_dict

def format_datetime(datetime_str):
    return datetime_str.replace(" ", "_").replace(":", "-")

def serialize_backtest_data(strategy_name, riskfree_rate=0.01, use_local_dash_url=False, version="1.0.0"):
    pickle_dict = prepare_data_for_pickle(strategy_name, riskfree_rate, use_local_dash_url, version)

    pkl_data_dir = f"{Path.home()}/backtest_data/"
    if not os.path.exists(pkl_data_dir):
        os.makedirs(pkl_data_dir)

    pkl_file_name = f"{strategy_name}_{format_datetime(observer_data.kline[0]['datetime'])}_to_{format_datetime(observer_data.kline[-1]['datetime'])}.pkl"
    pkl_file_path = os.path.join(pkl_data_dir, pkl_file_name)
    with open(pkl_file_path, 'wb') as pkl_file:
        pickle.dump(pickle_dict, pkl_file)

    return pkl_file_path
