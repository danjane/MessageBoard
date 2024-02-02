import socket
import sqlite3

db_file = 'message_board.db'


def get_host_ip():
    host_ = socket.gethostbyname(socket.gethostname())
    print(f"Server running on host = '{host_}'")
    return host_


def run(host_, conn):
    port = 13000

    udp_sock = setup_socket(host_, port)
    print("Waiting to receive messages...")
    while True:
        data, addr = receive(udp_sock)
        action_message(udp_sock, data, addr, conn)


def receive(udp_sock):
    data = None
    addr = None
    while not data:
        try:
            data, addr = udp_sock.recvfrom(1024)
            data = data.decode("utf-8")
            print(str(addr) + "> " + data)
        except Exception as e:
            print("Error during receive!!")
            print(e)
    return data, addr


def action_message(udp_sock, data, addr, conn):
    pieces = data.split("|")
    if pieces[0] == "AddAsListener":
        add_listener(udp_sock, pieces, addr, conn)
    elif pieces[0] == "AddAsSender":
        add_sender(conn, pieces, addr)
    else:
        message_id = store_message(pieces[0], addr, conn)
        if message_id:
            transmit_message(udp_sock, conn, message_id)


def store_message(message, addr, conn):
    cursor = conn.execute("INSERT INTO message(user_id, chat_id, content) VALUES(?, ?, ?)",
                 (1, 1, message))
    conn.commit()
    return cursor.lastrowid


def add_listener(udp_sock, data, addr, conn):
    print("Adding a new listener: " + str(addr))
    conn.execute("INSERT INTO listener(ip, port) VALUES (?, ?)",
                 (addr[0], addr[1]))
    replay_messages(udp_sock, addr, conn)


def replay_messages(udp_sock, addr_to, conn):
    query = conn.execute("SELECT content, user_id FROM message")
    for row in query.fetchall():
        udp_sock.sendto(bytearray(row[0], "utf-8"), addr_to)
    return None


def add_sender(conn, pieces, addr):
    if len(pieces) != 3:
        print("Expected 3 pieces as Command|Name|Password")
        return None
    _, name, password = pieces
    conn.execute('''
        UPDATE User
        SET ip = ?, port = ?
        WHERE name = ? AND password = ?
    ''', (addr[0], addr[1], name, password))

    conn.commit()


def transmit_message(udp_sock, conn, message_id):
    query = conn.execute('''
        SELECT Message.content, Message.message_date, User.name 
        FROM User JOIN Message ON Message.user_id == User.user_id 
        WHERE Message.message_id == ?
     ''', (message_id,))
    message, time, name = query.fetchone()

    query = conn.execute("SELECT ip, port FROM listener")
    listeners = query.fetchall()
    print(f"({str(time)}) {name}: {message} > " + str(listeners))
    for addr_to in listeners:
        udp_sock.sendto(bytearray(message, "utf-8"), addr_to)


def setup_socket(host_, port):
    server_addr = (host_, port)
    udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_sock.bind(server_addr)
    udp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    return udp_sock


if __name__ == "__main__":
    run(get_host_ip(), sqlite3.connect(db_file))
