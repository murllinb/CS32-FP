import sys
from threading import thread 
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


###### Game Logic #####
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

        if response is None: ###Chat suggested connectionerror
            raise ConnectionError(f"Player {player} disconnected.")

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

def game_session(conns: list[Socket32], addrs: list):
    players = ["X", "O"]
    scores  = {"X": 0, "O": 0, "Draws": 0}
 
    broadcast(conns, print_guide())
    while True:   # play again loop
        board   = [[" ", " ", " "] for _ in range(3)]
        current = 0  # 0 = X's turn, 1 = O's turn
 
        broadcast(conns, "\n  ================================")
        broadcast(conns, "         TIC  TAC  TOE")
        broadcast(conns, "  ================================")
        
        while True:   # single game loop
            player      = players[current]
            active_conn = conns[current]
            waiting_conn = conns[1 - current]
 
            board_str  = print_board(board)
            scores_str = f"  Scores  →  X: {scores['X']}  |  O: {scores['O']}  |  Draws: {scores['Draws']}"
 
            broadcast(conns, board_str)
            broadcast(conns, scores_str + "\n")
            send(waiting_conn, f"  Waiting for Player {player} to move...")    

            try:
                row, col = get_move(active_conn, board, player)
            except ConnectionError as e: ### Chat Suggested connection error inclusion
                broadcast(conns, f"\n  {e} Game over.")
                return            

            board[row][col] = player
 
            broadcast(conns, "\n  ================================")
            broadcast(conns, "         TIC  TAC  TOE")
            broadcast(conns, "  ================================")
 
            if check_winner(board, player):
                broadcast(conns, print_board(board))
                scores[player] += 1
                broadcast(conns, f"  Player {player} wins!\n")
                broadcast(conns, f"  Scores  →  X: {scores['X']}  |  O: {scores['O']}  |  Draws: {scores['Draws']}")
                break
 
            if is_draw(board):
                broadcast(conns, print_board(board))
                scores["Draws"] += 1
                broadcast(conns, "  It's a draw!\n")
                broadcast(conns, f"  Scores  →  X: {scores['X']}  |  O: {scores['O']}  |  Draws: {scores['Draws']}")
                break
 
            current = 1 - current
 
        # Ask both players if they want to play again (both must agree)
        broadcast(conns, "\n  Play again? (y/n): ")
        answers = []
        for conn in conns:
            ans = recv(conn)
            if ans is None:
                broadcast(conns, "  A player disconnected. Ending session.")
                return
            answers.append(ans.strip().lower())
 
        if all(a == "y" for a in answers):
            broadcast(conns, "\n  Both players want to play again! Starting new game...\n")
        else:
            broadcast(conns, "\n  Thanks for playing! Goodbye.\n")
            return



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
