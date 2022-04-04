import socket
import threading

HEADER = 64  # length of message in bytes(change to fit meter protocol length)
PORT = 5060
# SERVER = "192.168.1.19" #manual ip address fetch
SERVER = socket.gethostbyname(socket.gethostname())  # collect ip address automatically
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'  # encoding and decoding of messages
DISCONNECT_MESSAGE = "!DISCONNECT"  # server receives this message and disconnects the client

# make a socket to open device to connections
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)


# print(SERVER)

# handle communication between server & client
def handle_client(conn, addr):
    print(f"[NEW CONNECTION] {addr} connected")

    connected = True
    while connected:
        msg_length = conn.recv(HEADER).decode(FORMAT)  # insert message protocol here
        if msg_length:
            msg_length = int(msg_length)  # convert length to integer
            msg = conn.recv(msg_length).decode(FORMAT)
            if msg == DISCONNECT_MESSAGE:
                connected = False

            print(f"[{addr}] {msg}")
            conn.send("Msg received".encode(FORMAT))

    conn.close()


# handle new connections
def start():
    server.listen()
    print(f"[LISTENING] Server is listening on port: {PORT} ")
    while True:  # continuous listening
        conn, addr = server.accept()
        thread = threading.Thread(target=handle_client, args=(conn, addr))
        thread.start()
        print(f"[ACTIVE CONNECTIONS] {threading.active_count() - 1}")


print(f"[STARTING] server is starting on {ADDR}...")
start()
