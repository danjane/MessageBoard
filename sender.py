# Save as client.py 
# Message Sender
import socket

# host = "10.146.161.162" # set to IP address of target computer
host = '127.0.0.1'  # Loopback address for local testing
port = 13000
addr = (host, port)
UDPSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
UDPSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

name = input("Enter your name: ")
while True:
    message = input("Enter message: ")
    data = bytearray(name + "|" + message, "utf-8")
    UDPSock.sendto(data, addr)
