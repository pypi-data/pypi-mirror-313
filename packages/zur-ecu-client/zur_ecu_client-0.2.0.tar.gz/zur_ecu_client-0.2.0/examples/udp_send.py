"""
This example demonstrates how to send a UDP message to the ECU.
"""

import socket
import time

UDP_IP = "0.0.0.0"
UDP_PORT = 2020

data = b"test"

socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
while True:
    socket.sendto(data, (UDP_IP, UDP_PORT))
    print(f"Send message: {data} to {UDP_IP, UDP_PORT}")
    time.sleep(1)
