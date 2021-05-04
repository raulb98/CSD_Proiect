import os
import socket
import threading

HOST = "127.0.0.1"
PORT = 8080

CURRENT_USERS = []

def client_connected(conn, addr):
    get_user_info = False
    current_user = {
    "Nume" : None,
    "Conn" : conn,
    "Addr" : addr
    }
    while True:
        data = current_user["Conn"].recv(1024)
        print("Mesaj nou de la : {}".format(current_user["Nume"]))
        #if len(CURRENT_USERS) == 1:
        #    current_user["Conn"].sendall(b"Esti singur in Chat!")
        if get_user_info == False: # Prima oara cand un user se conecteaza trimite un mesaj in care are Numele de utilizator
            get_user_info = True
            current_user["Nume"] = data
            print("Nume : {}".format(str(data)))
            #current_user["Conn"].sendall(b"Te-ai conectat cu succes!")
            for user in CURRENT_USERS:
                if user[0] != current_user["Conn"]:
                    print("Trimis mesaj lui : {}".format(user[1]))
                    #user[0].sendall(bytes("S-a conectat : {}".format(current_user["Nume"]), 'utf-8'))
                    print("Am trimis mesaj lui {}".format(user[1]))
            continue
        if not data:
            break
        for user in CURRENT_USERS:
            if user[0] != current_user["Conn"]:
                user[0].sendall(data)


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    print("Server UP!")
    while True:
        server_socket.listen()
        conn, addr = server_socket.accept()
        CURRENT_USERS.append((conn, addr))
        threading.Thread(target=client_connected, args=(conn, addr, )).start()

if __name__ == "__main__":
    main()