# Save as server.py 
# Message Receiver
import socket


def get_host_ip():
    host = socket.gethostbyname(socket.gethostname())
    print(f"Server running on host = '{host}'")
    print("Changes needed in listener.py and sender.py\n")
    return host


def run(host):
    port = 13000

    udp_sock = setup_socket(host, port)
    messages = []
    listeners = []
    print("Waiting to receive messages...")
    while True:
        data, addr, message = receive(udp_sock)
        store_message(message, addr)
        if message == "AddAsListener":
            print("Adding a new listener: " + str(addr))
            listeners.append(addr)
            replay_messages(messages, addr)
        else:
            for listener_addr in listeners:
                print(message + str(addr))
                udp_sock.sendto(data, listener_addr)


def receive(udp_sock):
    message = None
    while not message:
        try:
            data, addr = udp_sock.recvfrom(1024)
            message = data.decode("utf-8")
        except Exception as e:
            print(e)
        print("Received message: " + message + " >from " + str(addr))
    return data, addr, message


def store_message(message, addr):
    pass


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

