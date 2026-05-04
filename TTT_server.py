import sys
from socket32 import Socket32, create_new_socket
 
HOST = sys.argv[1] if len(sys.argv) > 1 else "127.0.0.1"
PORT = int(sys.argv[2]) if len(sys.argv) > 2 else 9999

def send(conn: Socket32, message: str):
    conn.sendall(message + "\n")
 
def broadcast(conns: list[Socket32], message: str):
    for conn in conns:
        send(conn, message)
 
def recv(conn: Socket32) -> str | None:
    msg = conn.recv()
    if not msg:
        return None
    return msg.strip()

def handle_session(conns: list[Socket32], addrs: list):
        player_ids = [1, 2]
        for i, conn in enumerate(conns):
            send(conn, f"Welcome, Player {player_ids[i]}! Both players are connected.")
        broadcast(conns, "Game is ready to begin!\n")


###### Game logic #####
def print_board(board):
    print("\n")
    for row in range(3):
        # Build each row as " X | O |   " etc.
        cell1 = " " + board[row][0] + " "
        cell2 = " " + board[row][1] + " "
        cell3 = " " + board[row][2] + " "
        print("  " + cell1 + "|" + cell2 + "|" + cell3)
        if row < 2:
            print("  " + "-----------")
    print()

# Print a numbered guide so players know which number = which spot
def print_guide():
    print("  Position guide:")
    num = 1
    for row in range(3):
        cell1 = " " + str(num) + " ";   num += 1
        cell2 = " " + str(num) + " ";   num += 1
        cell3 = " " + str(num) + " ";   num += 1
        print("  " + cell1 + "|" + cell2 + "|" + cell3)
        if row < 2:
            print("  " + "-----------")
    print()

# Retur true if the given player has won
def check_winner(board, player):
    # Check each row
    for row in range(3):
        if board[row][0] == player and board[row][1] == player and board[row][2] == player:
            return True

    # Check each column
    for col in range(3):
        if board[0][col] == player and board[1][col] == player and board[2][col] == player:
            return True

    # Check top-left to bottom-right diagonal
    if board[0][0] == player and board[1][1] == player and board[2][2] == player:
        return True

    # Check top-right to bottom-left diagonal
    if board[0][2] == player and board[1][1] == player and board[2][0] == player:
        return True

    return False

# Return true if every cell is filled (no one won = draw)
def is_draw(board):
    for row in range(3):
        for col in range(3):
            if board[row][col] == " ":
                return False  # empty spot was found, so not a draw yet
    return True


def get_move(conn: Socket32, board, player: str):
    while True:
        send(conn, f"  Player {player}, enter position (1-9): ")
        response = recv(conn)
        if not response.isdigit():
            send(conn, "Invalid input. Enter a number 1-9.")
            continue

        move = int(response)
        if move < 1 or move > 9:
            send(conn, " Please enter a number between 1 and 9.")
            continue
 
        move_index = move - 1
        row = move_index // 3
        col = move_index % 3

        if board[row][col] != " ":
            send(conn, "  That spot is already taken! Try again.")
            continue
 
        return row, col






    broadcast(conns, "Placeholder: type anything and it will be echoed back.")
 
    while True:
        for i, conn in enumerate(conns):
            msg = recv(conn)
            if msg is None:
                broadcast(conns, f"Player {player_ids[i]} disconnected. Session ended.")
                return
            send(conn, f"Echo: {msg}")

def run():
    with create_new_socket() as server:
        server.bind(HOST, PORT)
        server.listen()
        print(f"[server] Listening on {HOST}:{PORT} — waiting for 2 players...")
 
        while True:
            conns, addrs = [], []
 
            for i in range(2):
                conn, addr = server.accept()
                conns.append(conn)
                addrs.append(addr)
                print(f"[server] Player {i + 1} connected from {addr}")
                send(conn, f"You are Player {i + 1}. Waiting for the other player...")
 
            print("[server] Both players connected. Starting session.")
            handle_session(conns, addrs)
            print("[server] Session ended. Ready for new players.\n")
 
 
if __name__ == "__main__":
    run()
