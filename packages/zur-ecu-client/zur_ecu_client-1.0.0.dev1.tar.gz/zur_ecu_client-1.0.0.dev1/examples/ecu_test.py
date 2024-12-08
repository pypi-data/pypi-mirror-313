"""
This is a simple example of how to send a message to the ECU using the UDP protocol.
After each sent message the script waits for a response from the ECU.
"""

import socket
import time


# Set the IP and port of the ECU
UDP_IP = "192.168.3.171"
UDP_PORT = 2020

data = b'[[{"bn":"ECU","n":"inverter","vs":"info"}]]'

socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
while True:
    socket.sendto(data, (UDP_IP, UDP_PORT))
    print(f"Send message: {data} to {UDP_IP, UDP_PORT}")
    print(socket.recvfrom(4096))
    time.sleep(1)
