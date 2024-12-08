import json
import logging
import sched
import time
from threading import Thread
from typing import Callable, Union

from zur_ecu_client.senml.senml_msg_dv import SenmlNames, Dv
from zur_ecu_client.udp_server import UdpServer
from zur_ecu_client.messages import Messages, Acknowledgment, Data

EcuClientListener = Callable[[Acknowledgment | Data], None]


class EcuClient:

    def __init__(
        self,
        listener: EcuClientListener,
        ecu_ip: str,
        ecu_port: int,
        client_ip: str = "0.0.0.0",
        client_port: int = 9000,
        calls_per_second: int = 1,
    ) -> None:
        logging.basicConfig(level=logging.CRITICAL)
        self.listener = listener
        self.requestInterval = 1.0 / calls_per_second
        self.subscriptions: list[SenmlNames] = []
        self.compiledMessages = []

        self.client_ip = client_ip
        self.client_port = client_port

        self.udpServer = UdpServer(self.client_ip, self.client_port, ecu_ip, ecu_port)

        self.thread1 = Thread(target=self.__receive_msg)
        # self.thread1.daemon = True
        self.thread2 = Thread(target=self.__schedule_requests)
        # self.thread2.daemon = True

    def start(self):
        self.thread1.start()
        self.thread2.start()

    def subscribe(self, data_field: Union[SenmlNames, str]):
        if type(data_field) is not SenmlNames and SenmlNames(data_field):
            data_field = SenmlNames(data_field)
        if data_field not in self.subscriptions:
            self.subscriptions.append(data_field)
        self.__compile_subscriptions()

    def unsubscribe(self, data_field: Union[SenmlNames, str]):
        if data_field in self.subscriptions:
            self.subscriptions.remove(data_field)
            self.__compile_subscriptions()

    def unsubscribe_all(self):
        self.subscriptions = []
        self.__compile_subscriptions()

    def send_msg(self, msg):
        if not msg:
            return
        msg = json.dumps(msg)
        self.udpServer.send_data(msg)

    def __compile_subscriptions(self):
        self.compiledMessages = []
        for entry in self.subscriptions:
            parameters = entry.value.split(":")
            compiled = [{"bn": parameters[0], "n": parameters[1], "vs": parameters[2]}]
            if compiled not in self.compiledMessages:
                self.compiledMessages.append(
                    [{"bn": parameters[0], "n": parameters[1], "vs": parameters[2]}]
                )

    def __receive_msg(self):
        while True:
            data = self.udpServer.receive_data()
            if data:
                try:
                    messages = Messages.parse(data)
                    self.listener(messages)
                    logging.info(f"Received -> {messages}")
                except Exception as error:
                    logging.error(f"{error} -> Could not parse message: {data}")

    def __request_messages(self):
        self.send_msg(self.compiledMessages)

    def __schedule_requests(self):
        scheduler = sched.scheduler(time.time, time.sleep)
        while True:
            scheduler.enter(self.requestInterval, 1, self.__request_messages, ())
            scheduler.run()
