import socket
import threading
import time

class FocusTimer:
    def __init__(self, session_length, break_length):
        self.session_length = session_length * 60
        self.break_length = break_length * 60
        self.current_time = 0
        self.is_study = True
        self.timer_started = False

    def start_timer(self, stop_event):
        self.timer_started = True
        while not stop_event.is_set():
            for self.current_time in range(self.session_length, 0, -1):
                self.is_study = True
                if stop_event.is_set():
                    break
                time.sleep(1)

            for self.current_time in range(self.break_length, 0, -1):
                self.is_study = False
                if stop_event.is_set():
                    break
                time.sleep(1)

    def get_time(self):
        status = "Study" if self.is_study else "Break"
        return f"{status}: {self.current_time // 60:02d}:{self.current_time % 60:02d}"

def handle_client(conn, addr, focus_timer, clients, stop_event):
    name = conn.recv(1024).decode('utf-8')
    clients[name] = conn
    print(f"Client {name} ({addr}) connected")
    print("Connected clients:", ", ".join(clients.keys()))

    if not focus_timer.timer_started:
        threading.Thread(target=focus_timer.start_timer, args=(stop_event,)).start()

    while not stop_event.is_set():
        try:
            conn.sendall(f"{focus_timer.get_time()} | Connected: {', '.join(clients.keys())}".encode('utf-8'))
            time.sleep(1)
        except (ConnectionResetError, BrokenPipeError):
            break

    print(f"Client {name} ({addr}) disconnected")
    del clients[name]
    print("Connected clients:", ", ".join(clients.keys()))
    conn.close()

def main():
    host = '0.0.0.0'
    port = 12345

    session_length = int(input("Enter session length (minutes): "))
    break_length = int(input("Enter break length (minutes): "))

    focus_timer = FocusTimer(session_length, break_length)
    clients = {}
    stop_event = threading.Event()

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    print(f"Server listening on {host}:{port}")

    try:
        while True:
            conn, addr = server.accept()
            threading.Thread(target=handle_client, args=(conn, addr, focus_timer, clients, stop_event)).start()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        stop_event.set()
        server.close()

if __name__ == "__main__":
    main()