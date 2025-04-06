import socket
import threading
import urllib.request
import requests  

public_ip = urllib.request.urlopen('https://api.ipify.org').read().decode('utf8')
print("[TEST] Public IP Address:", public_ip)

ip = ''
port = ''

def getdefaults():
    global ip, port  
    URL = "https://pastebin.com/raw/S26ywJmy"
    response = requests.get(URL)
    ip_port = response.text.strip()

    ip, port = ip_port.split(':')

    print(f"Detected Default IP/PORT {ip} : {port}")

getdefaults()



nickname = input("Enter nickname: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((ip, int(port)))


def receive():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
            else:
                print(message)
        except:
            print("network error occurred")
            client.close()
            break

def write():
    while True:
        message = f'{nickname}: {input()}'
        client.send(message.encode('ascii'))

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
