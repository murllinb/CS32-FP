# I will explain powerups.py
# to incentivize people to play the tournament style, you can translate your wins into coins
# Using your coins, you can buy powerups from the powerup shop. 
# the first powerup is cost 5 coins. Its called turn skipper. this adds a 1/6 chance 
# to dice 2 and three so that when you roll, theres a 1/6 chance you can skip your opponent's turn. 
# this means I would have to update dice.py and add an activation loop in the main game
# so that we can implement the powerups. everything will be stored locally, so should you
# end the tournament, none of the data is saved. 

def visit_shop(coins, inventory, player_name): 
  while True: 
    print(f"\n  ========================================")
    print(f"   {player_name.upper()}'S POWERUP SHOP")
    print(f"   Current Coins: {coins}")
    print(f"  ========================================")
    print("  [1] Turn Skipper (Cost: 5 Coins)")
    print("      - Gives a 1/6 chance to skip opponent's turn on a 'null' dice roll.")
    print("  [2] Mystery Powerup 1 (Cost: 7 Coins) - Coming Soon")
    print("  [3] Mystery Powerup 2 (Cost: 10 Coins) - Coming Soon")
    print("  [4] Mystery Powerup 3 (Cost: 15 Coins) - Coming Soon")
    print("  [N] No thanks, leave shop")

    choice = input(f"\n {player_name}, enter 1, 2, 3, 4 to buy respective powerup, or 'N' to leave: ").strip().lower()

    if choice == 'n': 
      print(" Leaving shop...bye bye buddy") 
      break 

    elif choice == '1': 
      if 1 in inventory: 
        print(" You already own the Turn Skipper!") 
      elif coins>= 5: 
        coins -= 5
        inventory.append(1)
        print(f" YAYAY: Bought Turn Skipper! You have {coins} coins left.") 
      else: 
        print(" Not enough coins! Get some more dubs...")
    elif choice in ['2', '3', '4']: 
      print(" I fear that powerup isn't available yet...") 
    else: 
      print(" Invalid choice. Try again...") 
      
  return coins, inventory 

def ask_to_activate(inventory, player_name): 
  # if they own powerup 1, ask if they to use it
  if 1 in inventory: 
    choice = input(f"\n {player_name}, do you want to activate 'Turn Skipper' for this round? (y/n): ").strip().lower()
    if choice == 'y': 
      print(" Turn Skipper Activated!") 
      return True # returns true if powerup 1 is activated
      
  return False # returns false if you dont own it or said no to activation. this boolean will be used in main




    

