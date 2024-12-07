import dash
from dash import dash_table
from dash import dcc, html
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import ffquant.plot.dash_ports as dash_ports
import getpass
import pandas as pd
import numpy as np
import psutil
import socket
import os
from ffquant.utils.Logger import stdout_log
from plotly.subplots import make_subplots
from datetime import datetime
import webbrowser
from ffquant.utils.dump_bt_data_utils import prepare_data_for_pickle, serialize_backtest_data
import time
import signal
import threading
import ffquant.utils.observer_data as observer_data

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
    close_order_price = close_order_info['execute_price']
    close_order_size = abs(close_order_info['execute_size'])
    close_order_type = close_order_info['order_type']

    pnl = 0
    if close_order_type == "Sell":
        pnl = (close_order_price - avg_open_price) * close_order_size
    else:
        pnl = (avg_open_price - close_order_price) * close_order_size
    return pnl

def analyze_trades(order_info_list: list, position_list: list = [], debug=False):
    closed_trades = []

    total_qty = 0.0
    total_cost = 0.0

    # 记录最新持仓 需要考虑初始值不为0的情况
    long_position = 0
    short_position = 0
    if len(position_list) > 0 and position_list[0]["position"] > 0:
        long_position = position_list[0]["position"]
    elif len(position_list) > 0 and position_list[0]["position"] < 0:
        short_position = abs(position_list[0]["position"])

    # 记录交易过程中的最大持仓
    max_long_position = 0
    max_short_position = 0
    order_origin_dict = dict()
    for order_info in order_info_list:
        order_timestamp = order_info['datetime']
        order_price = order_info['execute_price']
        order_size = order_info['execute_size']
        order_direction = order_info['order_type']
        order_origin = order_info['origin'] if order_info['origin'] is not None else "unknown"
        if debug:
            stdout_log(f"order_timestamp: {order_timestamp}, order_price: {order_price}, order_size: {order_size}, order_direction: {order_direction}, order_origin: {order_origin}")
        is_close_order = False
        
        if order_origin not in order_origin_dict.keys():
            order_origin_dict[order_origin] = 1
        else:
            order_origin_dict[order_origin] += 1
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
            if short_position < 0:
                long_position = abs(short_position)
                short_position = 0
        else:
            if long_position == 0:
                short_position += order_size
            else:
                long_position -= order_size
                is_close_order = True
            if long_position < 0:
                short_position = abs(long_position)
                long_position = 0
        
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
    reward_risk_ratio = avg_win_pnl / avg_loss_pnl if avg_loss_pnl > 0 else float('inf')

    win_rate = len(win_pnls) / len(closed_trades) if len(closed_trades) > 0 else 0
    
    # 计算每笔订单平均收益
    avg_return = sum([trade['pnl_return'] for trade in closed_trades]) / len(closed_trades) if len(closed_trades) > 0 else 0

    return reward_risk_ratio, win_rate, avg_return, max_long_position, max_short_position, order_origin_dict

def show_perf_graph(backtest_data, is_live=False, debug=False):
    strategy_name = backtest_data["strategy_name"]
    use_local_dash_url = backtest_data["use_local_dash_url"]

    port = dash_ports.get_available_port()
    username = getpass.getuser()
    username = username[8:] if username.startswith('jupyter-') else username
    app = init_dash_app(strategy_name, port, username, use_local_dash_url)

    init_table_callback(app, debug)
    init_graph_callback(app, debug)

    dt_range = f"{backtest_data['portfolio'][0]['datetime']} - {backtest_data['portfolio'][-1]['datetime']}"
    header = f"{strategy_name}[{dt_range}], created at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
    if is_live:
        header = f"{strategy_name}(live), created at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"

    interval = dcc.Interval(
        id='interval-component',
        interval=60*1000,
        n_intervals=0,
        max_intervals=0
    )
    if is_live:
        interval = dcc.Interval(
            id='interval-component',
            interval=60*1000,
            n_intervals=0
        )

    html_elements = []
    html_elements.append(html.H1(header, style={'textAlign': 'center'}))
    if is_live or len(observer_data.kline) > 0:
        html_elements.append(html.Button("Download Backtest Data", id="download-button", style={'position': 'absolute', 'top': '10px', 'right': '10px'}))
        html_elements.append(dcc.Download(id="download-backtest-data"))
        @app.callback(
            dash.dependencies.Output("download-backtest-data", "data"),
            [dash.dependencies.Input("download-button", "n_clicks")],
            prevent_initial_call=True
        )
        def download_backtest_data(n_clicks):
            if n_clicks:
                pkl_file_path = serialize_backtest_data(strategy_name, riskfree_rate=backtest_data["riskfree_rate"], use_local_dash_url=use_local_dash_url)
                return dcc.send_file(pkl_file_path)

    html_elements.append(dash_table.DataTable(
        id='metrics-table',
        style_cell={'textAlign': 'center'},
        style_header={
            'backgroundColor': 'lightgrey',
            'fontWeight': 'bold'
        },
        style_cell_conditional=[
            {'if': {'column_id': 'Metrics'}, 'width': '50%'},
            {'if': {'column_id': 'Result'}, 'width': '50%'}
        ],
        style_table={
            'width': '50%',
            'maxWidth': '800px',
            'margin': '0 auto'
        },
    ))
    html_elements.append(dcc.Graph(id='buysell-graph'))
    html_elements.append(interval)
    html_elements.append(dcc.Store(id='backtest-data-store', data=backtest_data))

    app.layout = html.Div(html_elements)

    if not is_live:
        TIMEOUT_SECONDS = 5

        @app.server.before_request
        def update_last_access_time():
            global dash_last_access_time
            dash_last_access_time = time.time()

        def monitor_timeout():
            global dash_last_access_time
            while True:
                time.sleep(5)
                if time.time() - dash_last_access_time > TIMEOUT_SECONDS:
                    if debug:
                        stdout_log("No activity detected. Shutting down server...")
                    os.kill(os.getpid(), signal.SIGTERM)
        threading.Thread(target=monitor_timeout, daemon=True).start()

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
        debug=True)

def init_table_callback(app, debug=False):
    @app.callback(
        Output('metrics-table', 'data'),
        [Input('interval-component', 'n_intervals')],
        [State('backtest-data-store', 'data')]
    )
    def update_metrics_table(n, data):
        backtest_data = data
        if n > 0:
            backtest_data = prepare_data_for_pickle(backtest_data["strategy_name"], backtest_data["riskfree_rate"], backtest_data["use_local_dash_url"])

        riskfree_rate = backtest_data["riskfree_rate"]
        portfolio = backtest_data["portfolio"]
        treturn = backtest_data["treturn"]
        order_info = backtest_data["order_info"]

        length = portfolio.__len__()
        if length > 0:
            days_in_year = 252
            minutes_in_day = 6.5 * 60
            total_return = portfolio[-1]['portfolio'] / portfolio[0]['portfolio'] - 1
            annual_return = "NaN"
            annual_return = (1 + total_return / (length / minutes_in_day)) ** days_in_year - 1
            std_per_minute = np.std([item['timereturn'] for item in treturn])
            std_annual = std_per_minute * np.sqrt(days_in_year * minutes_in_day)
            sharpe = "NaN"
            total_order_num = len(order_info)
            if std_annual != 0:
                sharpe = (annual_return - riskfree_rate) / std_annual

            reward_risk_ratio, win_rate, avg_return, max_long_position, max_short_position, order_origin_dict = analyze_trades(order_info, backtest_data["position"], debug=debug)
            if debug:
                stdout_log(f"reward_risk_ratio: {reward_risk_ratio}, win_rate: {win_rate}, avg_return: {avg_return}")

            metrics_data = {
                "Metrics": [
                    "总订单数量(买卖全量)",
                    "订单来源统计",
                    "区间总收益率",
                    "年化收益率",
                    "年化收益波动率",
                    "夏普比率",
                    "平均盈亏比",
                    "交易胜率",
                    "平仓单平均收益率",
                    "多头最大持仓量",
                    "空头最大持仓量"
                ],
                "Result": [
                    f"{total_order_num}",
                    f"{str(order_origin_dict)}",
                    f"{total_return:.8%}",
                    f"{annual_return:.8%}" if annual_return != "NaN" else annual_return,
                    f"{std_annual:.8%}" if std_annual != "NaN" else std_annual,
                    f"{sharpe:.8f}" if sharpe != "NaN" else sharpe,
                    f"{reward_risk_ratio:.8f}" if reward_risk_ratio != float('inf') else 'NaN',
                    f"{win_rate:.8%}",
                    f"{avg_return:.8%}",
                    f"{max_long_position}",
                    f"{max_short_position}"
                ]
            }
            return pd.DataFrame(metrics_data).to_dict('records')

def init_graph_callback(app, debug=False):
    @app.callback(
        Output('buysell-graph', 'figure'),
        Output('backtest-data-store', 'data'),
        [Input('interval-component', 'n_intervals')],
        [State('backtest-data-store', 'data')]
    )
    def update_graph(n, data):
        backtest_data = data
        if n > 0:
            backtest_data = prepare_data_for_pickle(backtest_data["strategy_name"], backtest_data["riskfree_rate"], backtest_data["use_local_dash_url"])

        # Fill K-line data
        kline_data = {
            "datetimes": [],
            "prices": []
        }
        for item in backtest_data["kline"]:
            kline_data['datetimes'].append(item["datetime"])
            kline_data['prices'].append(item["close"])

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
                x=kline_data['datetimes'],
                y=kline_data['prices'],
                mode='lines',
                name='Price'
            ),
            row=1, col=1  # First row, first column
        )

        # Handle buy points
        annotations = []
        for item in backtest_data["order_info"]:
            if item['order_type'] == "Buy":
                current_count = 0
                for annotation in annotations:
                    if annotation['x'] == item['datetime'] and (annotation['arrowcolor'] == "green" or annotation['arrowcolor'] == "purple"):
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
                        arrowcolor="green" if item['exec_type'] == "Market" else "purple",
                        hovertext=f"Position after trade: {item['position_after']}. Trade reason: {item['message']}",
                        ax=0,       # X-axis shift for the arrow (set to 0 for straight arrow)
                        ay=30       # Y-axis shift for the arrow
                    )
                )

        # Handle sell points
        for item in backtest_data["order_info"]:
            if item['order_type'] == "Sell":
                current_count = 0
                for annotation in annotations:
                    if annotation['x'] == item['datetime'] and (annotation['arrowcolor'] == "red" or annotation['arrowcolor'] == "black"):
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
                        arrowcolor="red" if item['exec_type'] == "Market" else "black",
                        hovertext=f"Position after trade: {item['position_after']}. Trade reason: {item['message']}",
                        ax=0,       # X-axis shift for the arrow
                        ay=-30      # Y-axis shift for the arrow
                    )
                )

        # Add portfolio line to the last row
        portfolio_data = {
            "datetimes": [],
            "values": []
        }
        for item in backtest_data["portfolio"]:
            portfolio_data['datetimes'].append(item["datetime"])
            portfolio_data['values'].append(item["portfolio"])
        figure.add_trace(
            go.Scatter(
                x=portfolio_data['datetimes'],
                y=portfolio_data['values'],
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
        ind_data = {
            "datetimes": kline_data["datetimes"]
        }
        keys = list(backtest_data["ind_data"].keys())
        for key in keys:
            if ind_data.get(key, None) is None:
                ind_data[key] = []

            for item in backtest_data["ind_data"][key]:
                ind_data[key].append(item)

            # Add indicator line to the second row
            figure.add_trace(
                go.Scatter(
                    x=ind_data['datetimes'],
                    y=ind_data[key],
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
        position_data = {
            "datetimes": kline_data["datetimes"],
            "values": []
        }
        for item in backtest_data["position"]:
            position_data['datetimes'].append(item["datetime"])
            position_data['values'].append(item["position"])
        figure.add_trace(
            go.Scatter(
                x=position_data['datetimes'],
                y=position_data['values'],
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
        drawdown_data = {
            "datetimes": [],
            "drawdowns": []
        }
        for item in backtest_data["drawdown"]:
            drawdown_data['datetimes'].append(item["datetime"])
            drawdown_data['drawdowns'].append(item["drawdown"])
        figure.add_trace(
            go.Scatter(
                x=drawdown_data['datetimes'],
                y=drawdown_data['drawdowns'],
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
            stdout_log(f"backtest_data: {backtest_data}")

        return figure, backtest_data