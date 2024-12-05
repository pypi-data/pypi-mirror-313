import dash
from dash import dash_table
from dash import dcc, html
from dash.dependencies import Input, Output, State
from ffquant.utils.dump_utils import dump_data_and_package
import plotly.graph_objs as go
import ffquant.utils.observer_data as observer_data
import ffquant.plot.dash_ports as dash_ports
import getpass
import plotly.express as px
import pandas as pd
import math
import numpy as np
import psutil
import socket
import os
import backtrader as bt
from ffquant.utils.Logger import stdout_log
from plotly.subplots import make_subplots
from datetime import datetime
import subprocess

__ALL__ = ['show_perf_live_graph', 'show_perf_bt_graph']

def get_self_ip():
    addrs = psutil.net_if_addrs()
    for _, interface_addresses in addrs.items():
        for address in interface_addresses:
            if address.family == socket.AF_INET and address.address.startswith('192.168.25.'):
                return address.address

def init_dash_app(strategy_name, port, username, use_local_dash_url=False):
    app = dash.Dash(
        name=strategy_name,
        requests_pathname_prefix=f"/user/{username}/proxy/{port}/" if not use_local_dash_url else None
    )
    app.title = strategy_name
    return app

def calculate_pnl(close_order_info, avg_open_price):
    close_order_price = close_order_info['data'].executed.price
    close_order_size = abs(close_order_info['data'].executed.size)
    close_order_type = close_order_info['data'].ordtype

    pnl = 0
    if close_order_type == bt.Order.Sell:
        pnl = (close_order_price - avg_open_price) * close_order_size
    else:
        pnl = (avg_open_price - close_order_price) * close_order_size
    return pnl

def analyze_trades(order_info_list):
    closed_trades = []

    total_qty = 0.0
    total_cost = 0.0

    last_order_info = None
    for order_info in order_info_list:
        order = order_info['data']
        order_price = order.executed.price
        order_size = abs(order.executed.size)

        if last_order_info is not None and abs(order_info['position_after']) < abs(last_order_info['position_after']):
            cur_avg_price = total_cost / total_qty
            pnl = calculate_pnl(order_info, cur_avg_price)

            closed_trades.append({
                'pnl': pnl,
                'pnl_return': pnl / (abs(order_info['data'].executed.size) * cur_avg_price),
                'is_win': pnl > 0
            })

            total_cost -= order_size * order_price
            total_qty -= order_size
        else:
            total_cost += order_size * order_price
            total_qty += order_size

        last_order_info = order_info

    win_pnls = [trade['pnl'] for trade in closed_trades if trade['pnl'] > 0]
    loss_pnls = [trade['pnl'] for trade in closed_trades if trade['pnl'] <= 0]
    total_order_count = len(order_info_list)

    avg_win_pnl = sum(win_pnls) / len(win_pnls) if len(win_pnls) > 0 else 0
    avg_loss_pnl = abs(sum(loss_pnls) / len(loss_pnls)) if len(loss_pnls) > 0 else 0
    risk_reward_ratio = avg_win_pnl / avg_loss_pnl if avg_loss_pnl > 0 else float('inf')

    win_rate = len(win_pnls) / total_order_count if total_order_count > 0 else 0

    avg_return = sum([trade['pnl_return'] for trade in closed_trades]) / len(closed_trades) if len(closed_trades) > 0 else 0

    return risk_reward_ratio, win_rate, avg_return

###########################################################
##################### Live Graph ##########################
###########################################################
def show_perf_live_graph(strategy_name, riskfree_rate=0.01, use_local_dash_url=False, debug=False):
    port = dash_ports.get_available_port()
    username = getpass.getuser()
    username = username[8:] if username.startswith('jupyter-') else username
    app = init_dash_app(strategy_name, port, username, use_local_dash_url)

    init_metrics_live_graph(app, riskfree_rate, debug)
    buysell_data = init_buysell_live_graph(app, debug)

    app.layout = html.Div([
        html.H1(f"{strategy_name}(live), created at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}", style={'textAlign': 'center'}),
        dash_table.DataTable(
            id='metrics-table',
            style_cell={'textAlign': 'left'},
            style_header={
                'backgroundColor': 'lightgrey',
                'fontWeight': 'bold'
            },
            style_cell_conditional=[
                {'if': {'column_id': 'Metrics'}, 'width': '50%'},
                {'if': {'column_id': 'Result'}, 'width': '50%'}
            ],
        ),
        dcc.Graph(id='buysell-graph'),
        dcc.Interval(
            id='interval-component',
            interval=60*1000,
            n_intervals=0
        ),
        dcc.Store(id='buysell-data-store', data=buysell_data)
    ])

    server_url = f"https://{os.environ.get('FINTECHFF_JUPYTERHUB_SERVER_URL', 'strategy.sdqtrade.com')}"
    if use_local_dash_url:
        server_url = f"http://{get_self_ip()}"

    app.run_server(
        host = '0.0.0.0',
        port = int(port),
        jupyter_mode = "jupyterlab",
        jupyter_server_url = server_url,
        use_reloader=False,
        debug=True)

######################## Live Overall Metrics #################
def init_metrics_live_graph(app, riskfree_rate = 0.01, debug=False):
    @app.callback(
        Output('metrics-table', 'data'),
        [Input('interval-component', 'n_intervals')]
    )
    def update_metrics_table(n_intervals):
        length = observer_data.portfolio.__len__()
        if length > 0:
            days_in_year = 252
            minutes_in_day = 6.5 * 60
            total_return = observer_data.portfolio[-1]['portfolio'] / observer_data.portfolio[0]['portfolio'] - 1
            annual_return = "NaN"
            if length > 60:
                annual_return = (1 + total_return / (length / minutes_in_day)) ** days_in_year - 1
            std_per_minute = np.std([item['timereturn'] for item in observer_data.treturn])
            std_annual = std_per_minute * np.sqrt(days_in_year * minutes_in_day)
            sharpe = "NaN"
            if std_annual != 0 and length > 60:
                sharpe = (annual_return - riskfree_rate) / std_annual

            profit_loss_ratio, win_rate, avg_return = analyze_trades(observer_data.order_info)
            if debug:
                stdout_log(f"profit_loss_ratio: {profit_loss_ratio}, win_rate: {win_rate}, avg_return: {avg_return}")

            metrics_data = {
                "Metrics": [
                    "区间总收益率",
                    "年化收益率",
                    "年化收益波动率",
                    "夏普比率",
                    "平均盈亏比",
                    "交易胜率",
                    "平仓单平均收益率"
                ],
                "Result": [
                    f"{total_return:.8%}",
                    f"{annual_return:.8%}" if annual_return != "NaN" else annual_return,
                    f"{std_annual:.8%}" if std_annual != "NaN" else std_annual,
                    f"{sharpe:.8f}" if sharpe != "NaN" else sharpe,
                    f"{profit_loss_ratio:.8f}",
                    f"{win_rate:.8%}",
                    f"{avg_return:.8%}"
                ]
            }
            return pd.DataFrame(metrics_data).to_dict('records')

######################## Live BuySell #######################
def init_buysell_live_graph(app, debug=False):
    buysell_data = {
        'datetimes': [],
        'prices': [],
        'buy_datetimes': [],
        'buy_prices': [],
        'sell_datetimes': [],
        'sell_prices': []
    }

    for key in observer_data.ind_data.keys():
        buysell_data[key] = []

    buysell_data['portfolio_datetimes'] = []
    buysell_data['portfolio_values'] = []

    buysell_data['position_datetimes'] = []
    buysell_data['position_values'] = []

    buysell_data['drawdown_datetimes'] = []
    buysell_data['drawdown_values'] = []

    @app.callback(
        Output('buysell-graph', 'figure'),
        Output('buysell-data-store', 'data'),
        [Input('interval-component', 'n_intervals')],
        [State('buysell-data-store', 'data')]
    )
    def update_buysell_graph(n, data):
        # Clear previous data
        data['datetimes'].clear()
        data['prices'].clear()

        # Fill K-line data
        for item in observer_data.kline:
            data['datetimes'].append(item["datetime"])
            data['prices'].append(item["close"])

        figure = make_subplots(
            rows=5, cols=1,
            shared_xaxes=True,  # Share X-axis between the plots
            vertical_spacing=0.05,
            row_heights=[2, 1, 1, 1, 1] # kline graph, indicator graph, portfolio graph, position graph, drawdown graph
        )

        # Add price line to the first row
        figure.add_trace(
            go.Scatter(
                x=data['datetimes'],
                y=data['prices'],
                mode='lines',
                name='Price'
            ),
            row=1, col=1  # First row, first column
        )

        # Handle buy points
        data['buy_datetimes'].clear()
        data['buy_prices'].clear()
        annotations = []
        for item in observer_data.order_info:
            if item['data'].ordtype == bt.Order.Buy:
                data['buy_datetimes'].append(item['datetime'])
                data['buy_prices'].append(item['data'].executed.price)

                current_count = 0
                for annotation in annotations:
                    if annotation['x'] == item['datetime'] and annotation['arrowcolor'] == "green":
                        current_count += 1
                close_price = None
                for kline in observer_data.kline:
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
        data['sell_datetimes'].clear()
        data['sell_prices'].clear()
        for item in observer_data.order_info:
            if item['data'].ordtype == bt.Order.Sell:
                data['sell_datetimes'].append(item['datetime'])
                data['sell_prices'].append(item['data'].executed.price)

                current_count = 0
                for annotation in annotations:
                    if annotation['x'] == item['datetime'] and annotation['arrowcolor'] == "red":
                        current_count += 1
                close_price = None
                for kline in observer_data.kline:
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
        data['portfolio_datetimes'].clear()
        data['portfolio_values'].clear()
        for item in observer_data.portfolio:
            data['portfolio_datetimes'].append(item["datetime"])
            data['portfolio_values'].append(item["portfolio"])
        figure.add_trace(
            go.Scatter(
                x=data['portfolio_datetimes'],
                y=data['portfolio_values'],
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
        keys = list(observer_data.ind_data.keys())
        for i in range(len(keys)):
            key = keys[i]
            if data.get(key, None) is None:
                data[key] = []
            else:
                data[key].clear()

            for item in observer_data.ind_data[key]:
                data[key].append(item)

            # Add indicator line to the second row
            figure.add_trace(
                go.Scatter(
                    x=data['datetimes'],
                    y=data[key],
                    mode='lines',
                    name=key
                ),
                row=2, col=1  # Second row, first column
            )

        # Update Y-axis title for each indicator subplot
        figure.update_yaxes(
            title_text="Indicators",
            row=2, col=1
        )

        # Add position line
        data['position_datetimes'].clear()
        data['position_values'].clear()
        for item in observer_data.position:
            data['position_datetimes'].append(item["datetime"])
            data['position_values'].append(item["position"])
        figure.add_trace(
            go.Scatter(
                x=data['position_datetimes'],
                y=data['position_values'],
                mode='lines',
                name='Position'
            ),
            row=3, col=1  # Last row, first column
        )
        figure.update_yaxes(
            title_text='Position',
            row=3, col=1
        )

        # Add drawdown line to the last row
        data['drawdown_datetimes'].clear()
        data['drawdown_values'].clear()
        for item in observer_data.drawdown:
            data['drawdown_datetimes'].append(item["datetime"])
            data['drawdown_values'].append(item["drawdown"])
        figure.add_trace(
            go.Scatter(
                x=data['drawdown_datetimes'],
                y=data['drawdown_values'],
                mode='lines',
                name='Drawdown'
            ),
            row=4, col=1  # Last row, first column
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

        if debug:
            stdout_log(f"buysell_data: {data}")

        return figure, data
    return buysell_data

###########################################################
################# Backtest Graph ##########################
###########################################################
def show_perf_bt_graph(strategy_name, riskfree_rate=0.01, use_local_dash_url=False, debug=False):
    executable_info = dump_data_and_package(strategy_name, use_local_dash_url, riskfree_rate, observer_data)
    exe_file_name = executable_info['exe_file_name']
    distpath = executable_info['distpath']
    try:
        result = subprocess.run([os.path.join(distpath, exe_file_name)], capture_output=True)
    except subprocess.CalledProcessError as e:
        stdout_log('Run exec file error:', e.stderr)

######################## Backtest Overall Metrics #################
def init_metrics_bt_graph(riskfree_rate = 0.01, debug=False):
    length = observer_data.portfolio.__len__()
    if length > 0:
        days_in_year = 252
        minutes_in_day = 6.5 * 60
        total_return = observer_data.portfolio[-1]['portfolio'] / observer_data.portfolio[0]['portfolio'] - 1
        annual_return = (1 + total_return / (length / minutes_in_day)) ** days_in_year - 1
        std_per_minute = np.std([item['timereturn'] for item in observer_data.treturn])
        std_annual = std_per_minute * np.sqrt(days_in_year * minutes_in_day)
        sharpe = "NaN"
        if std_annual != 0:
            sharpe = (annual_return - riskfree_rate) / std_annual

        risk_reward_ratio, win_rate, avg_return = analyze_trades(observer_data.order_info)

        if debug:
            stdout_log(f"risk_reward_ratio: {risk_reward_ratio}, win_rate: {win_rate}, avg_return: {avg_return}")

        metrics_data = {
            "Metrics": [
                "区间总收益率",
                "年化收益率",
                "年化收益波动率",
                "夏普比率",
                "平均盈亏比",
                "交易胜率",
                "平仓单平均收益率"
            ],
            "Result": [
                f"{total_return:.8%}",
                f"{annual_return:.8%}",
                f"{std_annual:.8%}" if std_annual != "NaN" else std_annual,
                f"{sharpe:.8f}" if sharpe != "NaN" else sharpe,
                f"{risk_reward_ratio:.8f}",
                f"{win_rate:.8%}",
                f"{avg_return:.8%}"
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

######################## Backtest Buysell #################
def init_buysell_bt_graph(debug=False):
    buysell_data = {
        'datetimes': [],
        'prices': [],
        'buy_datetimes': [],
        'buy_prices': [],
        'sell_datetimes': [],
        'sell_prices': []
    }

    for key in observer_data.ind_data.keys():
        buysell_data[key] = []

    buysell_data['position_datetimes'] = []
    buysell_data['position_values'] = []

    buysell_data['portfolio_datetimes'] = []
    buysell_data['portfolio_values'] = []

    buysell_data['drawdown_datetimes'] = []
    buysell_data['drawdown_values'] = []

    figure = make_subplots(
        rows=4, cols=1,
        shared_xaxes=True,  # Share X-axis between the plots
        vertical_spacing=0.05,
        row_heights=[2, 1, 1, 1] # kline graph, indicator graph, position graph, drawdown graph
    )

    # Add price line to the first row
    figure.add_trace(
        go.Scatter(
            x=[item["datetime"] for item in observer_data.kline],
            y=[item["close"] for item in observer_data.kline],
            mode='lines',
            name='Price'
        ),
        row=1, col=1  # First row, first column
    )

    # Handle buy points
    annotations = []  # Initialize annotations list
    for item in observer_data.order_info:
        # Add annotation for buy points
        if item['data'].ordtype == bt.Order.Buy:
            current_count = 0
            for annotation in annotations:
                if annotation['x'] == item['datetime'] and annotation['arrowcolor'] == "green":
                    current_count += 1
            close_price = None
            for kline in observer_data.kline:
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
    for item in observer_data.order_info:
        if item['data'].ordtype == bt.Order.Sell:
            current_count = 0
            for annotation in annotations:
                if annotation['x'] == item['datetime'] and annotation['arrowcolor'] == "red":
                    current_count += 1
            close_price = None
            for kline in observer_data.kline:
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
            x=[item["datetime"] for item in observer_data.kline],
            y=[item["portfolio"] for item in observer_data.portfolio],
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
    keys = list(observer_data.ind_data.keys())
    for i in range(len(keys)):
        key = keys[i]

        # Add indicator line to the second row
        figure.add_trace(
            go.Scatter(
                x=[item["datetime"] for item in observer_data.kline],
                y=[item for item in observer_data.ind_data[key]],
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
            x=[item["datetime"] for item in observer_data.kline],
            y=[item["position"] for item in observer_data.position],
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
            x=[item["datetime"] for item in observer_data.kline],
            y=[item["drawdown"] for item in observer_data.drawdown],
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