import socket
import threading
import urllib.request
import os
import sys

paste_url = "https://pastebin.com/raw/jkvhCMBD"

import urllib.request

import urllib.request

def getdefstats(paste_url):
    try:
        req = urllib.request.Request(
            paste_url,
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        with urllib.request.urlopen(req) as response:
            content = response.read().decode('utf-8').strip()
            ip, port = content.split(":")
            port = int(port)
            print("Default IP:", ip)
            print("Default Port:", port)
            return ip, port
    except Exception as e:
        print("Failed to get default stats:", e)
        return None, None

    
default_ip, default_port = getdefstats(paste_url)



def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    clear_screen()
    print("=" * 50)
    print("          Halewood Chat Roomz")
    print("=" * 50)
    print("Type your messages below. Press Ctrl+C to exit.\n")

public_ip = urllib.request.urlopen('https://api.ipify.org').read().decode('utf8')
print(f"[INFO] Your Public IP: {public_ip}")

nickname = input("Enter your nickname: ")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print("Leave blank for default")
ip = input("Server IP: ").strip()
port = input("Server Port: ").strip()


## making def port and ip 
if ip == "":
    ip = default_ip
if port == "":
    port = default_port
else:
    port = int(port)

client.connect((ip, port))


print_header()

def receive():
    while True:
        try:
            message = client.recv(1024).decode('ascii')

            if message == 'NICK':
                client.send(nickname.encode('ascii'))
            else:
                sys.stdout.write('\r')                  
                sys.stdout.flush()
                print(f"\n {message}")
                sys.stdout.write("> ")                 
                sys.stdout.flush()
        except:
            print("\n[ERROR] Network connection lost.")
            client.close()
            break

def write():
    while True:
        try:
            message = input("> ")
            full_message = f"{nickname}: {message}"
            client.send(full_message.encode('ascii'))
        except KeyboardInterrupt:
            print("\n[INFO] Exiting chat...")
            client.close()
            break

# Start threads
receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
