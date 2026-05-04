### import os and terminal clearing was a GAI suggestion to help deal with visual clutter, I commented out all the code that did the suggestion to show that the code still works w/o it.
import os

#import turtle 

from dice import roll_dice_one
from dice import roll_dice_two
from dice import roll_dice_three

from powerups import visit_shop, ask_to_activate

# Clear the terminal screen
def clear():
    os.system("cls" if os.name == "nt" else "clear")

# Print the current game board
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

# Return true if the given player has won
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

# Ask the player for a move and returns the row and column
# personalizing the game by asking the two players to input their names
def get_move(board, player, player_name):
    while True:
        try:
            move = int(input(f" {player_name} ({player}), enter position (1-9): "))

            if move < 1 or move > 9:
                print("  Please enter a number between 1 and 9.")
                continue

            # Convert 1-9 into row and column
            # e.g. move 5 → row 1, col 1 (middle)
            move_index = move - 1
            row = move_index // 3
            col = move_index % 3

            if board[row][col] != " ":
                print(" That spot is already taken! Try again.")
                continue

            return row, col

        except ValueError:
            print("  Invalid input. Enter a number 1-9.")

    

# def explain_dice_rules():
#     print("\n  ========================================================")
#     print("                    DICE POWER-UPS")
#     print("  ========================================================")
#     print("  Dice 1: 50% chance to replace opponent's piece, 50% to lose your turn.")
#     print("  Dice 2: 25% chance to replace opponent's piece, 25% to lose your turn,")
#     print("          50% chance of nothing (place piece normally).")
#     print("  Dice 3: ~17% (1/6) chance to replace opponent's piece, ~17% (1/6) to lose your turn,")
#     print("          ~66% (4/6) chance of nothing (place piece normally).")
#     print("  ========================================================\n")

def explain_dice_rules(): #Revised by ChatGPT to have cleaner formatting
    width = 80
    sep = ("=" * 58).center(width)
    indent = " " * ((width - 58) // 2)

    print()
    print(sep)
    print("DICE POWER-UPS".center(width))
    print(sep)
    lines = [
        "Dice 1: 50% chance to replace opponent's piece, 50% chance to lose turn.",
        "Dice 2: 25% chance to replace opponent's piece, 25% chance to lose turn,",
        "        50% chance of nothing (place piece normally).",
        "Dice 3: ~17% chance to replace opponent's piece, ~17% chance to lose turn,",
        "        ~66% chance of nothing (place piece normally).",
    ]
    for line in lines:
        print(indent + line)
    print(sep)
    print()

def print_streak(multiplier):
    print(f"X streak: {multiplier['X']['streak']} Best: {multiplier['X']['best_streak']}\n")
    print(f"O streak: {multiplier['O']['streak']} Best: {multiplier['O']['best_streak']}\n")

def main():
    is_new_tournament = True
    player_names = {}
    players = ["X", "O"]

    # keep track of coins
    scores = {"X": 0, "O":0, "Draws": 0}
    multiplier = {
        "X": {"streak": 0, "best_streak": 0},
        "O": {"streak": 0, "best_streak": 0}
    }
    coins = {"X": 0, "O": 0}
    inventory = {"X": [], "O": []}
    lastwinner = ""

    while True:
        clear()
        # print("\n  ================================")
        # print("        TIC  TAC  TOE")
        # print("  ================================")

        width = 80 #ChatGPT revised formatting
        sep = ("=" * 32).center(width)
        print()
        print(sep)
        print("TIC  TAC  TOE".center(width))
        print(sep)

        # since we are implementing tournaments, we don't want to print the rules every time. only if its a new game
        if is_new_tournament:
            explain_dice_rules()

            print("\n  ================================")
            print("  PLAYER SETUP")
            print("  ================================")
            player_names["X"] = input("  Enter name for Player X: ").strip() or "Player X"
            player_names["O"] = input("  Enter name for Player O: ").strip() or "Player O"

            # reset scoures for the new tournament
            scores = {"X": 0, "O": 0, "Draws": 0}
            coins = {"X": 0, "O": 0}
            inventory = {"X": [], "O": []}

        # now ask to activate the powerup should they have bought any
        active_powerups = {"X": False, "O": False}
        for p in players:
            active_powerups[p] = ask_to_activate(inventory[p], player_names[p])

        # make sure if powerup one is chosen, dice one is not
        dice_choices = {}
        print()

        dice_choices = {}

        print()
        for p in players:
            while True:
                # make sure powerup 1 and dice 1 are not used together
                if active_powerups[p] == True:
                    choice = input(f" {player_names[p]}, Powerup 1 is active, therefore you cannot use dice 1. Please pick 2 or 3: ").strip()
                    if choice in ['2', '3']:
                        dice_choices[p] = int(choice)
                        break
                    else:
                        print(" Invalid choice. Powerup 1 only works with dice 2 or 3...")
                else:
                    choice = input(f" {player_names[p]} (playing as {p}), choose your dice (1, 2, or 3): ").strip()
                    if choice in ['1', '2', '3']:
                        dice_choices[p] = int(choice)
                        break
                    else:
                        print(" Invalid choice. Please pick 1, 2, or 3.")

        # Need to initialize skipped turns before the game loop starts
        skipped_turns = {"X": False, "O": False}

        # Set up a blank 3x3 board filled with spaces
        board = [
            [" ", " ", " "],
            [" ", " ", " "],
            [" ", " ", " "]
        ]

        current = 0  # 0 = X's turn, 1 = O's turn

        print_guide()

        while True:
            player = players[current]
            opponent = players[1 if current == 0 else 0] # this way we can be more effective with dice uses
            current_name = player_names[player]

            # check if this player was skipped by the powerup 1
            if skipped_turns[player] == True:
                print(f"\n  ================================")
                print(f"  {current_name} IS SKIPPED!")
                print(f"  ================================")
                skipped_turns[player] = False # Turn off the skip for next time
                current = 1 if current == 0 else 0 # Switch to other player
                continue

            print_board(board)
            print(f"  Scores  →  {player_names['X']} (X): {scores['X']} |  {player_names['O']} (O): {scores['O']} |  Draws: {scores['Draws']}")
            print()

            # now we ask for rolling or placing
            action = ''
            while action not in ['roll', 'place']:
                action = input(f" Player {current_name}, do you want to 'roll' your dice or 'place' a piece? ")
                if action not in ['roll', 'place']:
                    print(" Please type 'roll' or 'place'. ")

            turn_used_by_dice = False
            opp_skipped = False

            if action == 'roll':
                dice_num = dice_choices[player]
                p1_active = active_powerups[player]

                # Dice is chosen. do the dice tasks and whether or not a removal happens
                if dice_num == 1:
                    turn_used_by_dice, opp_skipped = roll_dice_one(board, player, opponent)
                elif dice_num == 2:
                    turn_used_by_dice, opp_skipped = roll_dice_two(board, player, opponent, p1_active)
                elif dice_num == 3:
                    turn_used_by_dice, opp_skipped = roll_dice_three(board, player, opponent, p1_active)

                # is skip is used, apply it
                if opp_skipped == True:
                    skipped_turns[opponent] = True

            # if the player chose to place a piece or their dice roll didn't give a removal
            if action == 'place' or not turn_used_by_dice:
                row, col = get_move(board, player, current_name)
                board[row][col] = player

            # below part has been updated into above part
            # Ask for player move and place on board
            # row, col = get_move(board, player)
            # board[row][col] = player

            clear()
            print("\n  ================================")
            print("        TIC  TAC  TOE")
            print("  ================================")

            # Check if current player won
            if check_winner(board, player):
                print_board(board)
                scores[player] += 1 + multiplier[player]["streak"]
                coins[player] += 1 + mi
                if lastwinner == player: 
                    multiplier[player]["streak"] += 1
                    if multiplier[player]["streak"] > multiplier[player]["best_streak"]:
                        multiplier[player]["best_streak"] = multiplier[player]["streak"]
                else:
                    if lastwinner in ["X", "O"]:
                        multiplier[lastwinner]["streak"] = 0
                    lastwinner = player
    
                print(f"  {current_name} wins and has a coin multiplier of {multiplier[player]['streak']}x! (+{coins_earned} Coins)\n")
                print(f"  Scores  →  {player_names['X']} (X): {scores['X']} |  {player_names['O']} (O): {scores['O']} |  Draws: {scores['Draws']}")
                print_streak(multipler)
                break

            # Check if the board is full with no winner
            if is_draw(board):
                print_board(board)
                scores["Draws"] += 1
                lastwinner = ""
                print("  It's a draw!\n")
                print(f"  Scores  →  {player_names['X']} (X): {scores['X']} |  {player_names['O']} (O): {scores['O']} |  Draws: {scores['Draws']}")
                break

            # Switch to the other player (0 → 1, or 1 → 0)
            if current == 0:
                current = 1
            else:
                current = 0

# UPDATE: I am adding this in the end of the game, asking the players if they want to save their wins and continue
# playing like a tournament.

# post game menu...
        while True:
            print("\n  ========================================================")
            print("  WHAT WOULD YOU LIKE TO DO NEXT?")
            print("  ========================================================")
            print("  [S] VISIT SHOP: Spend your coins on powerups.")
            print("  [C] CONTINUE TOURNAMENT: Start next round.")
            print("  [N] START NEW GAME: Erase all scores, coins, and names.")
            print("  [Q] QUIT: Exit the game.")
            print("  ========================================================")

            again = input("  Choose S, C, N, or Q: ").strip().lower()

            if again == 's':
                shop_who = input(f"  Who wants to shop? Type 'X' for {player_names['X']} or 'O' for {player_names['O']}: ").strip().upper()
                if shop_who in ['X', 'O']:
                    # Call our simple shop function and update their coins/inventory
                    coins[shop_who], inventory[shop_who] = visit_shop(coins[shop_who], inventory[shop_who], player_names[shop_who])
                else:
                    print("  Invalid player.")
            elif again in ['c', 'n', 'q']:
                break # Break out of the menu loop to handle C, N, or Q

        if again == "q":
            print("\n  Thanks for playing gang! Have a swagalicious day.\n")
            break
        elif again == "n":
            is_new_tournament = True
        elif again == "c":
            is_new_tournament = False


        #print()
        #again = input("  Play again? (y/n): ").strip().lower()
        #if again != "y":
            #print("\n  Thanks for playing! Goodbye.\n")
            #break

if __name__ == "__main__":
    main()
