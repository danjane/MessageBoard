import socket

# Set up network connection
port = 13000
host = "192.168.1.115"
buffer = 1024
addr = (host, port)
UDPSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
UDPSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Ask server to be sent messages
UDPSock.sendto(bytearray("AddAsListener", "utf-8"), addr)

# Receive messages
print("Welcome to MessageBoard (listener)...")
while True:
    (data, addr) = UDPSock.recvfrom(buffer)
    message = data.decode("utf-8")
    print(message)
