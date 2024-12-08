import logging
import socket


class UdpServer:

    def __init__(self, udpIp: str, udpPort: int, remoteIp: str, remotePort: int):
        self.udpPort = udpPort
        self.udpIp = udpIp
        self.remotePort = remotePort
        self.remoteIp = remoteIp
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind((udpIp, udpPort))
        logging.info("Server is running on {}:{}".format(self.udpIp, self.udpPort))

    def receive_data(self):
        data, addr = self.socket.recvfrom(1024)
        data = data.decode("utf-8")
        logging.debug("Received from {}:{} -> {}".format(addr[0], addr[1], data))
        return data

    def send_data(self, data) -> None:
        data = data.encode("utf-8")
        self.socket.sendto(data, (self.remoteIp, self.remotePort))
        logging.debug(
            "Sent to {}:{} -> {}".format(self.remoteIp, self.remotePort, data)
        )

    def close(self):
        self.socket.close()
