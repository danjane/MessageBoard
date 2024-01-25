# Save as server.py 
# Message Receiver
import socket


def get_host_ip():
    host = socket.gethostbyname(socket.gethostname())
    print(f"Server running on host = '{host}'")
    print("Remember to change this in listener.py and sender.py")
    return host


def run():
    global messages
    host = '127.0.0.1'  # Loopback address for local testing
    port = 13000

    udp_sock = setup_socket(host, port)
    messages = []
    listeners = []
    print("Waiting to receive messages...")
    while True:
        data, addr, message, group = receive(udp_sock)
        store_message(message, group, addr)
        listeners = action_message(udp_sock, data, message, group, addr)


def receive(udp_sock):
    message = None
    while not message:
        try:
            data, addr = udp_sock.recvfrom(1024)
            package = data.decode("utf-8")
            print("Received package: " + package + " >from " + str(addr))
            group, message = safe_split(package)
        except Exception as e:
            print(e)
    return data, addr, message, group


def safe_split(package):
    pieces = package.split("|")
    if len(pieces) == 2:
        group, message = pieces
    else:
        group = None
        message = pieces
    return group, message


def store_message(message, group, addr):
    messages.append([message, group, addr])


def action_message(udp_sock, data, message, group, addr, listeners):
    if message == "AddAsListener":
        print("Adding a new listener: " + str(addr))
        listeners.append(addr)
        replay_messages(messages, addr)
    else:
        for listener_addr in listeners:
            print(message + str(addr))
            udp_sock.sendto(data, listener_addr)
    return listeners


def replay_messages(messages, addr):
    pass


def setup_socket(host, port):
    server_addr = (host, port)
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_sock.bind(server_addr)
    udp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    return udp_sock


if __name__ == "__main__":
    run(get_host_ip())

