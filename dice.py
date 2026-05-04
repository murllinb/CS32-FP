# Dice 1 will have a 50% chance of replacing your opponents piece and a 50% chance you lose your turn. 
# Dice 2 will have a 25% chance of replacing your opponents piece and a 25% chance of losing your turn. This means, 
# there is also a 50% chance that your dice rolls nothing siginificant, and should this happen, you are then prompted to 
# place down a piece as usual. 
# Dice 3 will have a 1/6 chance of replacing your opponents piece and a 1/6 chance of losing your turn. This means, 
# there is a 4/6 chance that your dice rolls nothing significant, and should this happen, you are then prompted to place 
# down a piece as usual. 
# If you do roll something of significance, after carrying out the dice's task, your turn will end. Meaning, should you get to 
# replace your opponent's piece or lose your turn, your turn will end after, and you will not get the chance to then
# place down a piece. 

import random 

# make a function that prompts you to replace a piece. make sure you are only replacing a piece for the available board space. 
def replace_piece(board, target_marker, replacement_marker): 
  piece_exists = False 
  for row in board: 
    if target_marker in row: 
      piece_exists = True 
      break 
      
  if not piece_exists: 
    print(f" No '{target_marker}' pieces on the board to replace! ")
    return False
    
  while True: 
    try: 
      move = int(input(f" Select a ' {target_marker} ' piece to replace (1-9): "))
      if move < 1 or move > 9:
        print("Please enter a number between 1-9.")
        continue
        
      move_index = move - 1
      row = move_index // 3
      col = move_index % 3

      if board[row][col] != target_marker:
        print(f"  That spot does not contain a '{target_marker}'. Try again...")
        continue
            
      # Replace the opponent's piece with the current player's marker
      board[row][col] = replacement_marker
      print(f"  '{target_marker}' piece replaced with '{replacement_marker}'!")
      return True
      
    except ValueError: 
      print("Numbers outside of 1-9 are invalid. Pick again...")


def roll_dice_one(board, current_player, opponent):
  roll = random.randint(1,6)
  print(f"\n  🎲 You rolled a {roll}!") 

  if roll in [1,2,3]: 
    print(f"  Awesome! You get to replace one of Player {opponent}'s pieces with your own.")
    return replace_piece(board, opponent, current_player) 
  else: # roll is 4,5,6
    print("  OH NO, you rolled too high. TURN SKIPPED WOMP WOMP")
    return True # Returning True skips the placement phase


# dice 2 will have a 1/4 chance for replacing opps piece or losing a turn. 1/2 chance for null and placing a piece like normal game play
def roll_dice_two(board, current_player, opponent):
  roll = random.randint(1,4)
  print(f"\n  🎲 You rolled a {roll}!") 

  if roll == 1:
    print(f"  You got a 1! You get to replace one of Player {opponent}'s pieces with your own.")
    return replace_piece(board, opponent, current_player)  
  elif roll == 4:
    print("  OH NO, you rolled a 4. TURN SKIPPED WOMP WOMP")
    return True
  else: # if roll in 2 or 3 
    print(f" No special moves! Place down a piece like regular-smegular.")
    return False


# dice 3 will have a 1/6 chance for replacing opps piece or losing a turn. 4/6 chance for null and placing a piece like normal game play
def roll_dice_three(board, current_player, opponent):
  roll = random.randint(1,6)
  print(f"\n  🎲 You rolled a {roll}!")

  if roll == 1: 
    print(f"  Awesome! You get to replace one of Player {opponent}'s pieces with your own.")
    return replace_piece(board, opponent, current_player)
  elif roll == 6: 
    print("  OH NO, you rolled too high. TURN SKIPPED WOMP WOMP")
    return True 
  else: 
    print("  Nothing significant happened! You must place down a piece...")
    return False
