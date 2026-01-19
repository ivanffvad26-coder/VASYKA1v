#Разработчик мессанжера Vasyka, Иванов Вадим Александрович
print("SERVER FILE STARTED")
import socket
HOST = "127.0.0.1"
PORT = 5000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

print(f"Сервер запущен на {HOST}:{PORT}")

while True:
    conn, addr = server.accept()
    print(f"Подключился клиент: {addr}")

    message = conn.recv(1024).decode("utf-8")
    print("Сообщение:", message)

    conn.send("Сообщение получено сервером".encode("utf-8"))
    conn.close()
