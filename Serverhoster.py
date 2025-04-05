import threading
import socket

import time 

encrypt_string = "AKSDLLMIIIN"

password = encrypt_string[0] + encrypt_string[3] + encrypt_string[6] + encrypt_string[7] + encrypt_string[10] 
host = '192.168.1.123' # local host


while True:
    x = str(input("Password"))
    x = x.upper()
    if x != "ADMIN":
        input("incorrect Password")
    else:
        print("\n  Access Granted")
        break

port = int(input("enter a port "))
servername = input("What do you want your room to be called")

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host,port))
server.listen()
print("ver 1.7")
clients = []
nicknames = []

def broadcast(message):
    for client in clients:
        client.send(message)
    

def handle(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames[index]
            nicknames.remove(nickname)
            broadcast(f"{nickname} Has left  {servername}".encode('ascii'))
            


def receive():
    while True:
        client, address = server.accept()

        

        client.send('NICK'.encode('ascii'))
        nickname = client.recv(1024).decode('ascii')
        nicknames.append(nickname)
        clients.append(client)        


        print(f"the Nick of the client is {nickname} they jsut connected to {servername}")

        broadcast(f"{nickname} Just joined {servername} \n All Connected users {nicknames}".encode('ascii'))
        client.send("".encode('ascii'))

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()



print("server is listening... ")
receive()