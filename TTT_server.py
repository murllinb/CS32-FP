import sys
from threading import Thread 
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
    output = "\n"
    for row in range(3):
        cell1 = " " + board[row][0] + " "
        cell2 = " " + board[row][1] + " "
        cell3 = " " + board[row][2] + " "
        output += "  " + cell1 + "|" + cell2 + "|" + cell3 + "\n"
        if row < 2:
            output += "  -----------\n"
    return output   

# Print a numbered guide so players know which number = which spot
def print_guide():
    output = "  Position guide:\n"
    num = 1
    for row in range(3):
        cell1 = " " + str(num) + " ";   num += 1
        cell2 = " " + str(num) + " ";   num += 1
        cell3 = " " + str(num) + " ";   num += 1
        output += "  " + cell1 + "|" + cell2 + "|" + cell3 + "\n"
        if row < 2:
            output += "  -----------\n"
    return output  


def check_winner(board, player):
    for row in range(3):
        if board[row][0] == player and board[row][1] == player and board[row][2] == player:
            return True

    for col in range(3):
        if board[0][col] == player and board[1][col] == player and board[2][col] == player:
            return True

    if board[0][0] == player and board[1][1] == player and board[2][2] == player:
        return True

    if board[0][2] == player and board[1][1] == player and board[2][0] == player:
        return True

    return False

def is_draw(board):
    for row in range(3):
        for col in range(3):
            if board[row][col] == " ":
                return False
    return True


def get_move(conn: Socket32, board, player: str):
    while True:
        send(conn, f"  Player {player}, enter position (1-9): ")
        response = recv(conn)

        if response is None:
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

    while True:
        board   = [[" ", " ", " "] for _ in range(3)]
        current = 0
 
        broadcast(conns, "\n  ================================")
        broadcast(conns, "         TIC  TAC  TOE")
        broadcast(conns, "  ================================")
        
        while True:
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
            except ConnectionError as e:
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
            game_session(conns, addrs)  
            print("[server] Session ended. Ready for new players.\n")
 
 
if __name__ == "__main__":
    run()
