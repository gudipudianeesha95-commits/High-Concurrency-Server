import socket
import time

HOST = "127.0.0.1"
PORT = 5000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server.bind((HOST, PORT))
server.listen(100)

print(f"Blocking server started on {HOST}:{PORT}")

while True:
    conn, addr = server.accept()

    print(f"Client connected: {addr}")

    data = conn.recv(1024)

    print(f"Received: {data.decode()}")

    # Simulate 100 ms of I/O waiting
    time.sleep(0.1)

    response = "Hello from Blocking Server!"

    conn.sendall(response.encode())

    conn.close()