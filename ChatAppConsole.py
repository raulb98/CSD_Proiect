import socket
import threading
from RC6 import RC6

HOST = '127.0.0.1'
PORT = 8080

MY_DATA = {
    "Name" : None,
    "Nr_messages" : 0
}

def recv_from_chat(client_socket, rc6):
    first_msg = True
    while True:
        data = client_socket.recv(1024)
        data = str(data, 'utf-8')
        data = rc6.decrypt(data)
        print(data)

def send_to_chat(client_socket, rc6):
    while True:
        data_to_send = input("Text: ")
        message = "{};{}".format(MY_DATA["Name"], data_to_send)
        message = rc6.encrypt(message)
        print(message)
        client_socket.sendall(bytes(message, "utf-8"))

def enter_chat():
    rc6 = RC6("A WORD IS A WORD")
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    client_socket.sendall(MY_DATA["Name"])
    recv_thread = threading.Thread(target=recv_from_chat, args=(client_socket, rc6))
    recv_thread.start()
    send_thread = threading.Thread(target=send_to_chat, args=(client_socket, rc6))
    send_thread.start()

def main():
    name = input("Enter your name: ")
    MY_DATA["Name"] = bytes(name, "utf-8")
    enter_chat()

if __name__ == "__main__":
    main()