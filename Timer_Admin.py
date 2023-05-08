import socket
import sys

def main():
    host = input("Enter the server IP address: ")
    port = 12345

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((host, port))
    except ConnectionRefusedError:
        print("Unable to connect to the server. Check if the server is running and the IP address is correct.")
        sys.exit(1)

    client.sendall("admin".encode('utf-8'))
    response = client.recv(1024).decode('utf-8')
    if response != "OK":
        print("Unable to connect as admin.")
        sys.exit(1)

    print("Connected as admin.")
    print("Commands:")
    print("  update_lengths <session_length> <break_length>")
    print("  send_message <message>")

    while True:
        command = input("> ")
        if command.startswith("update_lengths") or command.startswith("send_message"):
            client.sendall(command.encode('utf-8'))
        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()