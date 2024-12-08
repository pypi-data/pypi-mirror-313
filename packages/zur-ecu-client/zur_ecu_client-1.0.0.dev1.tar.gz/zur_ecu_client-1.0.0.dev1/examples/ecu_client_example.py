"""
Example usage of the ECU client.
"""

import logging
import time
from zur_ecu_client.senml.senml_msg_dv import Dv
from zur_ecu_client.senml.senml_zur_names import SenmlNames
from zur_ecu_client.messages import Acknowledgment, Data
from zur_ecu_client.ecu_client import EcuClient


def ecu_message_listener(message: Acknowledgment | Data):
    if isinstance(message, Acknowledgment):
        logging.info(f"Received acknowledgment: {message}")
    elif isinstance(message, Data):
        logging.info(f"Received data: {message}")
    else:
        logging.warning(f"Received unknown message type: {message}")


def main():
    logging.basicConfig(level=logging.INFO)

    # Initialize ECU client
    ecu_ip = "0.0.0.0"
    ecu_port = 2020
    client_ip = "0.0.0.0"
    client_port = 9000
    calls_per_second = 1

    ecu_client = EcuClient(
        ecu_message_listener, ecu_ip, ecu_port, client_ip, client_port, calls_per_second
    )

    ecu_client.start()

    # Subscribe to messages
    ecu_client.subscribe(SenmlNames.ECU_ACCU_ACTUATOR)

    test_message = Dv.Control(1, 1, 1).get()

    try:
        while True:
            ecu_client.send_msg(test_message)
            time.sleep(1)
    except KeyboardInterrupt:
        ecu_client.udpServer.close()
        logging.info("ECU client stopped")


if __name__ == "__main__":
    main()
