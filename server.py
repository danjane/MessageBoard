import socket
import sqlite3


db_file = 'message_board.db'


def get_host_ip():
    host_ = socket.gethostbyname(socket.gethostname())
    print(f"Server running on host = '{host_}'")
    return host_


host = get_host_ip()


def run(host_, conn):
    port = 13000

    udp_sock = setup_socket(host_, port)
    messages = []
    listeners = []
    print("Waiting to receive messages...")
    while True:
        data, addr, message = receive(udp_sock)
        store_message(data, addr, conn)
        if message == "AddAsListener":
            print("Adding a new listener: " + str(addr))
            listeners.append(addr)
            replay_messages(udp_sock, addr, conn)
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
            print("Error during receive!!")
            print(e)
        print("Received message: " + message + " >from " + str(addr))
    return data, addr, message


def store_message(data, addr, conn):
    conn.executemany("INSERT INTO raw(ip, port, data) VALUES(?, ?, ?)",
                     [(addr[0], addr[1], data)])
    conn.commit()
    return None


def replay_messages(udp_sock, addr, conn):
    result = conn.execute("SELECT data FROM raw")
    for data in result.fetchall():
        udp_sock.sendto(data[0], addr)
    return None


def setup_socket(host_, port):
    server_addr = (host_, port)
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_sock.bind(server_addr)
    udp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    return udp_sock


if __name__ == "__main__":
    conn = sqlite3.connect(db_file)
    run(host, conn)

