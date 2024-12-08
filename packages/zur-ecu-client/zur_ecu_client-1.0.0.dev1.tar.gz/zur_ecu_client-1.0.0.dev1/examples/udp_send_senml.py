"""
This example demonstrates how to send and receive SenML message from the ECU using UDP.
"""

import socket
import json

# Set the IP and port of the ECU
ECU_IP = "0.0.0.0"
ECU_PORT = 9000

# SenML message to be send
data = [
    [
        {"bn": "ECU", "n": "driverless", "vs": "control"},
        {"n": "steeringAngle", "u": "°", "v": -2000},
    ]
]

MESSAGE = json.dumps(data)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

# Send message
sock.sendto(MESSAGE.encode(), (ECU_IP, ECU_PORT))
print(f"Send msg: {MESSAGE}")

# Receive message
response, addr = sock.recvfrom(1024)
response = response.decode()
print(f"Received msg: {response}")
