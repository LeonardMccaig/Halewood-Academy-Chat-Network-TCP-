import socket
import threading
import os
import time

import os

def cls():
    os.system('cls' if os.name=='nt' else 'clear')

# Now, to clear the screen
cls()

COLORS = {
    "RESET": "\033[0m",
    "BOLD": "\033[1m",
    "CYAN": "\033[96m",
    "GREEN": "\033[92m",
    "YELLOW": "\033[93m",
    "RED": "\033[91m",
}

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    clear_screen()
    print(f"{COLORS['CYAN']}{COLORS['BOLD']}=== halewood Academy Chat roomz ==={COLORS['RESET']}\n")

def get_port():
    while True:
        print_banner()
        print("Options:\n1) Global Chat\n2) Private Chat")
        choice = input(f"{COLORS['YELLOW']}Enter your choice (1 or 2): {COLORS['RESET']}")

        if choice == "1":
            return 8008
        elif choice == "2":
            try:
                return int(input(f"{COLORS['YELLOW']}Enter your custom port (Room number): {COLORS['RESET']}"))
            except ValueError:
                print(f"{COLORS['RED']}Invalid port. Please enter a number.{COLORS['RESET']}")
        else:
            print(f"{COLORS['RED']}Invalid choice. Please enter 1 or 2.{COLORS['RESET']}")

port = get_port()
nickname = input(f"{COLORS['GREEN']}Enter your nickname: {COLORS['RESET']}")
cls()

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('192.168.1.123', port))

def receive():
    while True:
        try:
            message = client.recv(1024).decode('ascii')
            if message == 'NICK':
                client.send(nickname.encode('ascii'))
            else:
                print(f"{COLORS['CYAN']}{message}{COLORS['RESET']}\n{COLORS['GREEN']}{COLORS['RESET']}", end="", flush=True)
        except:
            print(f"\n{COLORS['RED']}Network ERROR occurred. Likely, the server was closed.{COLORS['RESET']}")
            client.close()
            break

def write():
    while True:
        message = input(f"{COLORS['YELLOW']}You: {COLORS['RESET']}")
        if len(message) > 200:
            print(f"{COLORS['RED']}Message exceeds 200 characters. Please shorten your message.{COLORS['RESET']}")
            continue
        formatted_message = f"{nickname}: {message}"
        client.send(formatted_message.encode('ascii'))
        time.sleep(2)  # 2-second cooldown

receive_thread = threading.Thread(target=receive, daemon=True)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()
