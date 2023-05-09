import socket
import os
import sys

def main():
    host = input("Enter the server IP address: ")
    port = 12345

    # AF_INET IPV4  Address Family
    # SOCK_STREAM TCP connection 
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((host, port))
    except ConnectionRefusedError:
        print("Unable to connect to the server. Check if the server is running and the IP address is correct.")
        sys.exit(1)

    name = input("Enter your name: ")
    client.sendall(name.encode('utf-8'))

    while True:
        # .recv blocking call that reads atmost 1024 bytes
        timer = client.recv(1024).decode('utf-8')
        os.system('clear' if os.name == 'posix' else 'cls')
        print(timer)

if __name__ == "__main__":
    main()
#10.22.75.104
