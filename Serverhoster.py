import socket
import threading

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("localhost", 9999))
server.listen()

clients = []
nicknames = []

def broadcast(message):
    for client in clients:
        client.send(message)

def sendclients2client(client):
    client.send("Clients in the room:\n".encode('ascii'))
    
    for nickname in nicknames:
        client.send(f" [{nickname}]\n".encode('ascii'))


        

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
            broadcast(f"\n {nickname} has left the room ".encode("ascii"))
            break

def receive():
    while True:
        client, addr = server.accept()
        print("Client connected with IP", addr)

        client.send('NICK'.encode("ascii"))
        nickname = client.recv(1024).decode("ascii")
        nicknames.append(nickname)
        clients.append(client)

        print(f"Nickname of the client is {nickname}")
        broadcast(f"{nickname} just joined the Room!\n ".encode("ascii"))
        
        sendclients2client(client)

        thread = threading.Thread(target=handle, args=(client,))
        thread.start()

print("Listening on port 9999...")
receive()
