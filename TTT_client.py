import random
from threading import thread 
from socket32 import create_new_socket

HOST = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
PORT = int(sys.argv[2]) if len(sys.argv) > 2 else 9999

##dumb client - sends and recieves text 

def main():

  #receieve what servers assigns X and O 
  #display
  #one client sends a move to server

  def receive(conn: Socket32):
    """Listen to server messages and print them."""
    while True:
        msg = conn.recv()
        if not msg:
            print("\n[client] Disconnected from server.")
            break
        print(msg, end="")  # server already includes newlines


def send(conn: Socket32):
    """Read user input and send to server."""
    while True:
        try:
            user_input = input()
            conn.sendall(user_input + "\n")
        except (EOFError, ConnectionError):
            break

#main function 
def run():
    with create_new_socket() as client:
        client.connect(HOST, PORT)
        print(f"[client] Connected to {HOST}:{PORT}")

        # Start listening thread
        Thread(target=receive, args=(client,), daemon=True).start()

        # Main thread handles user input
        send(client)


if __name__ == '__main__':
    run()
