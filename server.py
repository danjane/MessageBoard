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
    listeners = []
    print("Waiting to receive messages...")
    while True:
        data, addr = receive(udp_sock)
        store_message(data, addr, conn)
        action_message(udp_sock, data, addr, conn)


def receive(udp_sock):
    data = None
    while not data:
        try:
            data, addr = udp_sock.recvfrom(1024)
            data = data.decode("utf-8")
            print("Received message: " + data + " >from " + str(addr))
        except Exception as e:
            print("Error during receive!!")
            print(e)
    return data, addr


def store_message(data, addr, conn):
    conn.executemany("INSERT INTO raw(ip, port, data) VALUES(?, ?, ?)",
                     [(addr[0], addr[1], data)])
    conn.commit()
    return None


def action_message(udp_sock, data, addr, conn):
    pieces = data.split("|")
    if pieces[0] == "AddAsListener":
        add_listener(data, addr, conn)
    elif pieces[0] == "AddAsSender":
        print("todo")
    else:
        listeners = conn.execute("SELECT ip, port FROM listener")
        for addr in listeners.fetchall():
            print(data + str(addr))
            udp_sock.sendto(bytearray(data, "utf-8"), addr)


def add_listener(udp_sock, addr, conn):
        print("Adding a new listener: " + str(addr))
        conn.execute("INSERT INTO listener(ip, port) VALUES (?, ?)",
                     (addr[0], addr[1]))
        replay_messages(udp_sock, addr, conn)


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

