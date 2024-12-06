from datetime import datetime
import json
from confluent_kafka import Producer

__ALL__ = ['MqProducer']

class MqProducer():
    def __init__(self, *args, **kwargs):
        conf = {
            'bootstrap.servers': '192.168.25.148:9092',
            'client.id': f"MqProducer_{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        }
        self.producer = Producer(conf)

    def start(self):
        pass

    def send(self, symbol="", type_name="", millis=0, data=None, data_type=None):
        """
        发送消息到 Kafka 的方法

        参数：
        - symbol: 标的符号，默认为空字符串
        - type_name: 消息类型名称，默认为空字符串
        - millis: 当前时间戳（毫秒）
        - data: 实际数据，默认为 None
        - data_type: 数据类型，默认为 None
        """
        # 处理时间戳字段
        time_open = millis
        time_close = millis + 60 * 1000

        # 处理类型和符号，防止包含不合法字符
        sanitized_type_name = str(type_name).replace('|', '_')
        sanitized_symbol = str(symbol).replace('|', '_')

        # 决定 signal_key 和 signal_value 的内容
        signal_key = "data" if data_type is None else str(data_type).replace('|', '_')
        signal_value = json.dumps({'data': data}) if data_type is None else json.dumps(data)
        sanitized_signal_value = signal_value.replace('|', '_')

        # 构造消息值
        value = (
            f"{time_open}|"
            f"{time_close}|"
            f"{sanitized_type_name}|"
            f"{sanitized_symbol}|"
            f"{signal_key}|"
            f"{sanitized_signal_value}"
        )

        # 发送消息到 Kafka
        self.producer.produce("t_index_info_data", key="", value=value)
        self.producer.flush()