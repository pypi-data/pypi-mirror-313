import pickle
import os
import sys
from dash import dash_table
from dash import dcc, html
from plotly.subplots import make_subplots
import plotly.graph_objs as go
import ffquant.plot.dash_ports as dash_ports
from ffquant.plot.dash_graph import init_dash_app, get_self_ip
from ffquant.utils.Logger import stdout_log
import getpass
import datetime
import pandas as pd
import numpy as np
import backtrader as bt
import webbrowser
import threading
import time
import signal


def calculate_pnl(close_order_info, avg_open_price):
    close_order_price = close_order_info['execute_price']
    close_order_size = abs(close_order_info['execute_size'])
    close_order_type = close_order_info['order_type']

    pnl = 0
    if close_order_type == "Sell":
        pnl = (close_order_price - avg_open_price) * close_order_size
    else:
        pnl = (avg_open_price - close_order_price) * close_order_size
    return pnl

def analyze_trades(order_info_list: list):
    closed_trades = []

    total_qty = 0.0
    total_cost = 0.0

    # 记录最新持仓
    long_position = 0
    short_position = 0
    # 记录交易过程中的最大持仓
    max_long_position = 0
    max_short_position = 0
    for order_info in order_info_list:
        order_timestamp = order_info['datetime']
        order_price = order_info['execute_price']
        order_size = order_info['execute_size']
        order_direction = order_info['order_type']
        is_close_order = False
        
        # 将持仓分为两部分：多头持仓和空头持仓
        # 如果产生 Buy 订单：
        #  - 如果空头仓位为0，则代表多头仓位在加仓，那么就继续累加到多头仓位上；
        #  - 如果空头仓位不为0， 则代表空头仓位在平仓，那么就减少对应空头的仓位。
        # 如果产生 Sell 订单：
        #  - 如果多头仓位为0，则代表空头仓位在加仓，那么继续累加到空头仓位上；
        #  - 如果多头仓位不为0，则代表多头仓位在平仓，那么就减少对应多头的仓位。
        # 加仓和平仓后需要重新计算之前仓位的平均成本。
        #  - 如果全部仓位被平掉，则给 total_cost 和 total_qty 设为 0。
        #  - 如果部分仓位被平掉，则给 total_cost 和 total_qty 减去平掉的部分。
        if order_direction == "Buy":
            if short_position == 0:
                long_position += order_size
            else:
                short_position -= order_size
                is_close_order = True
        else:
            if long_position == 0:
                short_position += order_size
            else:
                long_position -= order_size
                is_close_order = True
        
        if is_close_order:
            cur_avg_price = total_cost / total_qty
            pnl = calculate_pnl(order_info, cur_avg_price)

            closed_trades.append({
                'datetime': order_timestamp,
                'pnl': pnl,
                'pnl_return': pnl / (abs(order_info['execute_size']) * cur_avg_price),
                'is_win': pnl > 0
            })

            if total_qty == order_size:
                total_cost = 0
                total_qty = 0
            else:
                total_cost -= order_size * order_price
                total_qty -= order_size
        else:
            total_cost += order_size * order_price
            total_qty += order_size
            
        max_long_position = long_position if long_position > max_long_position else max_long_position
        max_short_position = short_position if short_position > max_short_position else max_short_position

    win_pnls = [trade['pnl'] for trade in closed_trades if trade['is_win']]
    loss_pnls = [trade['pnl'] for trade in closed_trades if not trade['is_win']]

    avg_win_pnl = sum(win_pnls) / len(win_pnls) if len(win_pnls) > 0 else 0
    avg_loss_pnl = abs(sum(loss_pnls) / len(loss_pnls)) if len(loss_pnls) > 0 else 0
    
    # 计算盈亏比
    risk_reward_ratio = avg_win_pnl / avg_loss_pnl if avg_loss_pnl > 0 else float('inf')

    win_rate = len(win_pnls) / len(closed_trades) if len(closed_trades) > 0 else 0
    
    # 计算每笔订单平均收益
    avg_return = sum([trade['pnl_return'] for trade in closed_trades]) / len(closed_trades) if len(closed_trades) > 0 else 0

    return risk_reward_ratio, win_rate, avg_return, max_long_position, max_short_position

def init_metrics_bt_graph(backtest_data, riskfree_rate=0.01, debug=False):
    length = backtest_data["portfolio"].__len__()
    if length > 0:
        days_in_year = 252
        minutes_in_day = 6.5 * 60
        total_return = backtest_data["portfolio"][-1]["portfolio"] / backtest_data["portfolio"][0]["portfolio"] - 1
        annual_return = (1 + total_return / (length / minutes_in_day)) ** days_in_year - 1
        std_per_minute = np.std([item['timereturn'] for item in backtest_data["treturn"]])
        std_annual = std_per_minute * np.sqrt(days_in_year * minutes_in_day)
        sharpe = "NaN"
        total_order_num = len(backtest_data["order_info"]) if backtest_data["order_info"] != None else 0
        if std_annual != 0:
            sharpe = (annual_return - riskfree_rate) / std_annual

        risk_reward_ratio, win_rate, avg_return, max_long_position, max_short_position = analyze_trades(backtest_data["order_info"])

        if debug:
            stdout_log(f"risk_reward_ratio: {risk_reward_ratio}, win_rate: {win_rate}, avg_return: {avg_return}")

        metrics_data = {
            "Metrics": [
                "Total Number of Orders(Buy and Sell)",
                "Total Return",
                "Annualized Return",
                "Annual Return Volatility",
                "Sharpe Ratio",
                "Risk Reward Ratio",
                "Win Rate",
                "Close Order Average Return",
                "Max Long Position",
                "Max Short Position"
            ],
            "Result": [
                f"{total_order_num}",
                f"{total_return:.8%}",
                f"{annual_return:.8%}",
                f"{std_annual:.8%}" if std_annual != "NaN" else std_annual,
                f"{sharpe:.8f}" if sharpe != "NaN" else sharpe,
                f"{risk_reward_ratio:.8f}",
                f"{win_rate:.8%}",
                f"{avg_return:.8%}",
                f"{max_long_position}",
                f"{max_short_position}"
            ]
        }

        metrics_df = pd.DataFrame(metrics_data)
        return dash_table.DataTable(
                data=metrics_df.to_dict('records'),
                style_cell={'textAlign': 'left'},
                style_header={
                    'backgroundColor': 'lightgrey',
                    'fontWeight': 'bold'
                },
                style_cell_conditional=[
                    {'if': {'column_id': 'Metrics'}, 'width': '50%'},
                    {'if': {'column_id': 'Result'}, 'width': '50%'}
                ]
        )

def init_buysell_bt_graph(backtest_data):
    figure = make_subplots(
        rows=4, cols=1,
        shared_xaxes=True,  # Share X-axis between the plots
        vertical_spacing=0.05,
        row_heights=[2, 1, 1, 1], # kline graph, indicator graph, position graph, drawdown graph
        specs=[
            [{"secondary_y": True}],  # The first row enables secondary y
            [{}],  # The second row
            [{}],  # The third row
            [{}],  # The fourth row
        ]
    )

    # Add price line to the first row
    figure.add_trace(
        go.Scatter(
            x=[item["datetime"] for item in backtest_data["kline"]],
            y=[item["close"] for item in backtest_data["kline"]],
            mode='lines',
            name='Price'
        ),
        row=1, col=1  # First row, first column
    )

    # Handle buy points
    annotations = []  # Initialize annotations list
    for item in backtest_data["order_info"]:
        # Add annotation for buy points
        if item['order_type'] == "Buy":
            current_count = 0
            for annotation in annotations:
                if annotation['x'] == item['datetime'] and annotation['arrowcolor'] == "green":
                    current_count += 1
            close_price = None
            for kline in backtest_data["kline"]:
                if kline['datetime'] == item['datetime']:
                    close_price = kline['close']
                    break
            annotations.append(
                dict(
                    x=item['datetime'],
                    y=close_price - 10 * current_count,
                    xref="x",
                    yref="y",
                    showarrow=True,
                    arrowhead=2,
                    arrowsize=1,
                    arrowcolor="green",
                    ax=0,       # X-axis shift for the arrow (set to 0 for straight arrow)
                    ay=30       # Y-axis shift for the arrow
                )
            )

    # Handle sell points
    for item in backtest_data["order_info"]:
        if item['order_type'] == "Sell":
            current_count = 0
            for annotation in annotations:
                if annotation['x'] == item['datetime'] and annotation['arrowcolor'] == "red":
                    current_count += 1
            close_price = None
            for kline in backtest_data["kline"]:
                if kline['datetime'] == item['datetime']:
                    close_price = kline['close']
                    break
            annotations.append(
                dict(
                    x=item['datetime'],
                    y=close_price + 10 * current_count,
                    xref="x",
                    yref="y",
                    showarrow=True,
                    arrowhead=2,
                    arrowsize=1,
                    arrowcolor="red",
                    ax=0,       # X-axis shift for the arrow
                    ay=-30      # Y-axis shift for the arrow
                )
            )
            
    # Add portfolio line to the last row
    figure.add_trace(
        go.Scatter(
            x=[item["datetime"] for item in backtest_data["kline"]],
            y=[item["portfolio"] for item in backtest_data["portfolio"]],
            mode='lines',
            name='Portfolio'
        ),
        row=1, col=1,
        secondary_y=True
    )
    figure.update_yaxes(
        title_text='Portfolio',
        row=1, col=1,
        secondary_y=True
    )

    # Add indicator data to the second row
    keys = list(backtest_data["ind_data"].keys())
    for i in range(len(keys)):
        key = keys[i]

        # Add indicator line to the second row
        figure.add_trace(
            go.Scatter(
                x=[item["datetime"] for item in backtest_data["kline"]],
                y=[item for item in backtest_data["ind_data"][key]],
                mode='lines',
                name=key
            ),
            row=2, col=1
        )

    # Update Y-axis title for each indicator subplot
    figure.update_yaxes(
        title_text="Indicators",
        row=2, col=1
    )

    # Add position line
    figure.add_trace(
        go.Scatter(
            x=[item["datetime"] for item in backtest_data["kline"]],
            y=[item["position"] for item in backtest_data["position"]],
            mode='lines',
            name='Position'
        ),
        row=3, col=1
    )
    figure.update_yaxes(
        title_text='Position',
        row=3, col=1
    )

    # Add drawdown line to the last row
    figure.add_trace(
        go.Scatter(
            x=[item["datetime"] for item in backtest_data["kline"]],
            y=[item["drawdown"] for item in backtest_data["drawdown"]],
            mode='lines',
            name='Drawdown'
        ),
        row=4, col=1
    )
    figure.update_yaxes(
        title_text='Drawdown',
        row=4, col=1
    )

    # Add annotations to the layout
    figure.update_layout(
        title='BuySells and Indicators',
        xaxis=dict(title='Time', type='category'),
        yaxis=dict(title='Price'),
        height=400 * 6,
        annotations=annotations
    )

    return dcc.Graph(
        id="buysell-graph",
        figure=figure
    )

def new_path(file_path):
    return os.path.abspath(os.path.join(os.path.dirname(__file__), file_path))

def main():
    # 获取当前运行的目录（兼容打包后和未打包时的情况）
    if getattr(sys, 'frozen', False):
        # 如果是打包后的可执行文件
        pkl_path = new_path('./backtest_data.pkl')
    else:
        # 如果是未打包的 Python 脚本
        current_dir = os.path.dirname(os.path.abspath(__file__))
        pkl_path = os.path.join(current_dir, 'backtest_data.pkl')

    # 读取 PICKLE 文件
    backtest_data = None
    with open(pkl_path, 'rb') as pickle_file:
        backtest_data = pickle.load(pickle_file)

    strategy_name = backtest_data['strategy_name']
    use_local_dash_url = backtest_data['use_local_dash_url']
    riskfree_rate = backtest_data['riskfree_rate']

    port = dash_ports.get_available_port()
    username = getpass.getuser()
    username = username[8:] if username.startswith('jupyter-') else username
    app = init_dash_app(strategy_name, port, username, use_local_dash_url)

    last_access_time = time.time()
    timeout_seconds = 5  # 超时时间：5分钟
    
    # 回调函数记录访问时间
    @app.server.before_request
    def update_last_access_time():
        global last_access_time
        last_access_time = time.time()

    # 检查超时并关闭服务器
    def monitor_timeout():
        global last_access_time
        while True:
            time.sleep(5)  # 每5秒检查一次
            if time.time() - last_access_time > timeout_seconds:
                print("No activity detected. Shutting down server...")
                # 关闭服务器
                os.kill(os.getpid(), signal.SIGTERM)

    # 启动超时检测线程
    threading.Thread(target=monitor_timeout, daemon=True).start()

    dt_range = f"{backtest_data['portfolio'][0]['datetime']} - {backtest_data['portfolio'][-1]['datetime']}"
    app.layout = html.Div([
        html.H1(f"{strategy_name}[{dt_range}], created at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", style={'textAlign': 'center'}),
        init_metrics_bt_graph(backtest_data, riskfree_rate=riskfree_rate),
        init_buysell_bt_graph(backtest_data),
    ])

    server_url = f"https://{os.environ.get('FINTECHFF_JUPYTERHUB_SERVER_URL', 'strategy.sdqtrade.com')}"
    if use_local_dash_url:
        server_url = f"http://{get_self_ip()}"

    webbrowser.open(f"http://{get_self_ip()}:{int(port)}")
    app.run_server(
        host = '0.0.0.0',
        port = int(port),
        jupyter_mode = "jupyterlab",
        jupyter_server_url = server_url,
        use_reloader=False,
        debug=True
    )


if __name__ == '__main__':
    main()