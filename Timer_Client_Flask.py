from flask import Flask, render_template, request
import socket
import threading
import sys

app = Flask(__name__)

host = None
port = 12345
name = None
timer = None
client = None

def receive_timer():
    global timer
    while True:
        timer = client.recv(1024).decode('utf-8')

@app.route('/')
def index():
    return render_template('index.html', name=name, timer=timer)

@app.route('/timer')
def get_timer():
    return timer

if __name__ == "__main__":
    host = input("Enter the server IP address: ")
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((host, port))
    except ConnectionRefusedError:
        print("Unable to connect to the server. Check if the server is running and the IP address is correct.")
        sys.exit(1)

    name = input("Enter your name: ")
    client.sendall(name.encode('utf-8'))

    threading.Thread(target=receive_timer, daemon=True).start()

    app.run(debug=True)