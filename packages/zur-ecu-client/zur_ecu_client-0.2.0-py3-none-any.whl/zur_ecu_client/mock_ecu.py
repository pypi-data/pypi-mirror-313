import json
import logging
import time
import csv


from zur_ecu_client.messages import Acknowledgment, Data, Messages
from zur_ecu_client.senml.senml import Senml
from zur_ecu_client.udp_server import UdpServer
from zur_ecu_client.senml.senml_msg_ecu import Ecu
from zur_ecu_client.senml.senml_zur_names import *


class MockECU:

    def __init__(self, mock_ecu_ip: str, mock_ecu_port: int, dv_ip: str, dv_port: int):
        logging.basicConfig(level=logging.DEBUG)
        self.mock_ecu_ip = mock_ecu_ip
        self.mock_ecu_port = mock_ecu_port
        self.dv_ip = dv_ip
        self.dv_port = dv_port
        self.udp_server = UdpServer(mock_ecu_ip, mock_ecu_port, dv_ip, dv_port)

    @staticmethod
    def do_every(period, f, *args):
        def g_tick():
            t = time.time()
            while True:
                t += period
                yield max(t - time.time(), 0)

        g = g_tick()
        while True:
            time.sleep(next(g))
            f(*args)

    def response_msg(self, mock_data: list):

        mission_msgs, accu_msgs, velocity_msgs, error_msgs = mock_data
        mission_count = 0

        while True:
            data = self.udp_server.receive_data()
            if data:

                data = Messages.parse2(data)

                for element in data:
                    result = []

                    if mission_count >= len(mission_msgs):
                        return

                    # if element is a Request from Client
                    if type(element) is Acknowledgment:
                        base: Senml.Base = element.base
                        base_name = base.bn + base.n + base.v
                        if base_name == SenmlNames.ECU_ACCU_SENSOR.value:
                            result = accu_msgs[mission_count]
                        elif base_name == SenmlNames.ECU_INVERTER_ACTUAL.value:
                            result = velocity_msgs[mission_count]
                        elif base_name == SenmlNames.ECU_ERROR_INFO.value:
                            result = error_msgs[mission_count]
                        elif base_name == SenmlNames.ECU_TEMPORARY_INFO.value:
                            if mission_count >= len(mission_msgs):
                                return
                            else:
                                result = mission_msgs[mission_count]
                                mission_count += 1
                        else:
                            result = []
                        # result = get_mock_data(mock_data, base.n)

                        self.udp_server.send_data(json.dumps(result))

                    # if element is a Data from Client
                    elif type(element) is Data:

                        base: Senml.Base = element.base
                        send = {
                            "bn": str(base.bn).replace(":", ""),
                            "n": str(base.n).replace(":", ""),
                            "vs": str(base.v).replace(":", ""),
                        }
                        self.udp_server.send_data(str(send))


def __main__():
    client_ip = "127.0.0.1"
    client_port = 9000
    mock_ecu_ip = "127.0.0.1"
    mock_ecu_port = 9001
    mock_ecu = MockECU(mock_ecu_ip, mock_ecu_port, client_ip, client_port)
    try:
        demo_data = [[], [], [], []]
        with open("../Demo.csv", "r") as f:
            reader = csv.reader(f, delimiter=",")
            for i, line in enumerate(reader):
                if i == 0:
                    pass
                if i > 0:
                    demo_data[0].append(
                        Ecu.Temporary(
                            available=line[0] == "TRUE" if line[0] != "" else False,
                            mission_sel=int(line[1]) if line[1] != "" else None,
                            mission_ack=int(line[2]) if line[2] != "" else None,
                            startup=line[3] == "TRUE" if line[3] != "" else False,
                            shutdown=line[4] == "TRUE" if line[4] != "" else False,
                        ).get()
                    )
                    demo_data[1].append(
                        Ecu.Accu(
                            charge=int(line[5]) if line[5] != "" else None,
                            temp=int(line[6]) if line[6] != "" else None,
                        ).get()
                    )
                    demo_data[2].append(
                        Ecu.Inverter(
                            velocity=int(line[7]) if line[7] != "" else None,
                        ).get()
                    )
                    demo_data[3].append(
                        Ecu.Error(
                            error_icon=line[8] if line[8] != "" else None,
                            error_message=line[9] if line[9] != "" else None,
                        ).get()
                    )
        mock_ecu.response_msg(demo_data)
        # mock_ecu.do_every(1, mock_ecu.response_msg, msgs)
    except KeyboardInterrupt:
        mock_ecu.udp_server.close()


if __name__ == "__main__":
    __main__()
