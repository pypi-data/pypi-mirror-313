import os
import pickle
import subprocess
import platform
from datetime import datetime
import pytz
import backtrader as bt
from ffquant.utils.Logger import stdout_log

# 当前工具路径
utils_folder_path = os.path.dirname(os.path.abspath(__file__))
# 在用户根目录创建 backtest_exe 文件夹用于存放回测的可执行文件
executable_file_path = os.path.join(os.path.expanduser("~"), "backtest_exe") if platform.system() == 'Linux' else os.path.join(os.path.expanduser("~"), "backtest_exe")
os.makedirs(executable_file_path, exist_ok=True)


def executable_file_pack(user_exe_path, strategy_name, pickle_data_file):
    split_symbol = ':' if platform.system() == 'Linux' else ';'
    now_datetime_str = datetime.now(pytz.timezone('Asia/Hong_Kong')).strftime('%Y-%m-%d_%H_%M_%S')
    package_exe_command = [
        'pyinstaller',
        '--onefile',
        "--add-data", f"{os.path.join(pickle_data_file, 'backtest_data.pkl')}{split_symbol}.",
        '--name', f'{strategy_name}_{now_datetime_str}',
        '--distpath', f'{user_exe_path}',
        f"{os.path.join(pickle_data_file, 'executable_dash_plot.py')}"
    ]
    try:
        subprocess.run(
            package_exe_command,
            check=True
        )
    except subprocess.CalledProcessError as e:
        stdout_log("打包失败: ", e)
        
    return f'{strategy_name}_{now_datetime_str}'

def dump_data_and_package(strategy_name, use_local_dash_url, riskfree_rate, observer_data):
    pickle_dict = {}
    pickle_dict["strategy_name"] = strategy_name
    pickle_dict["use_local_dash_url"] = use_local_dash_url
    pickle_dict["riskfree_rate"] = riskfree_rate
    # 下面的数据不能直接存，因为依赖关系太复杂，无法全部打包进入 exe，会有 hidden-module 被丢弃，导致最终的 exe 不可用
    pickle_dict['treturn'] = observer_data.treturn
    pickle_dict['portfolio'] = observer_data.portfolio
    pickle_dict['buysell'] = observer_data.buysell
    pickle_dict['drawdown'] = observer_data.drawdown
    pickle_dict['kline'] = observer_data.kline
    pickle_dict['position'] = observer_data.position
    pickle_dict['ind_data'] = observer_data.ind_data
    
    pickle_dict = wash_order_info(observer_data, pickle_dict)
    
    pickle_data_file = os.path.join(utils_folder_path,'backtest_data.pkl')
    with open(pickle_data_file, 'wb') as pickle_file:
        pickle.dump(pickle_dict, pickle_file)
        
    exe_file_name = executable_file_pack(executable_file_path, strategy_name, utils_folder_path)
    
    return {'exe_file_name': exe_file_name, 'distpath': executable_file_path}
        

def wash_order_info(observer_data, pickle_dict):
    order_list = list()
    for item in observer_data.order_info:
        tmp_order_dict = dict()
        tmp_order_dict['datetime'] = item['datetime']
        tmp_order_dict['order_type'] = "Buy" if item['data'].ordtype == bt.Order.Buy else "Sell"
        tmp_order_dict['execute_price'] = item['data'].executed.price
        tmp_order_dict['execute_size'] = abs(item['data'].executed.size)
        tmp_order_dict['position_after'] = item['position_after']
        order_list.append(tmp_order_dict)
    
    pickle_dict['order_info'] = order_list
    return pickle_dict