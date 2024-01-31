import socket
import server

port = 13000
addr = (server.host, port)
UDPSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
UDPSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

name = input("Enter your name: ")
while True:
    message = input("Enter message: ")
    data = bytearray(name + "> " + message, "utf-8")
    UDPSock.sendto(data, addr)
