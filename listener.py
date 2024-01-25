import socket

# Set up network connection
# host = "10.146.161.162" # set to IP address of target computer
host = '127.0.0.1'  # Loopback address for local testing
port = 13000
buffer = 1024
addr = (host, port)
UDPSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
UDPSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

# Ask server to be sent messages
UDPSock.sendto(bytearray("AddAsListener", "utf-8"), addr)

# Receive messages
print("Welcome to MessageBoard...s")
while True:
    (data, addr) = UDPSock.recvfrom(buffer)
    message = data.decode("utf-8")
    print(message)
