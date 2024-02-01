import socket
import server

print("Welcome to MessageBoard (sender)...")

# Set up socket
port = 13000
addr = (server.host, port)
UDPSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
UDPSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Log in as user
name = input("Enter your name: ")
pwd = input("Enter your password: ")
data = bytearray("AddAsSender|" + name + "|" + pwd, "utf-8")
UDPSock.sendto(data, addr)

# Send messages
while True:
    message = input("Enter message: ")
    data = bytearray(message, "utf-8")
    UDPSock.sendto(data, addr)
