# CS32-FP
CS32 FP by [Murllin Bender,  Elisabeth Lai, Siya Patel]

Our project is a take on the infamous Tic-Tac-Toe game. This game "Dice Tic-Tac-Toe" can have two players alternating between turns, laying down X's and O's on a 3x3 9 piece board. After they get three in a row, they win! --- Unlike normal Tic-Tac-Toe, this take has unique dices with powerups that the player can choose from. Theres three different dices that users can choose like characters --- and they have unique attributes. When its a player's turn, they can choose whether or not to roll it or play like normal. These dices will keep the game unique and interesting. We have a an overall game system where scores and streaks are tracked across rounds. Additionally, there is a shop system where users can buy items with the coins they earn after every round. Lastly, our new feauture we implemented is Turtle, a drawing system that sketches out the board in the terminal.

Instructions:
In order to play Dice Tic-Tac-Toe, you first need to install basegame.py and dice.py, then run basegame.py. 
  Game Instructions:
1. Have each player pick which symbol they want to be (X) and (O)
2. Have each player pick which dice they want to use:
  * Extreme Dice: 1/2 odds of removing your opponents piece or your piece
  * Intermediate Dice: 1/4 odds of removing your opponents piece or your piece and 1/2 odds of nothing happening.
  * Beginnner Dice:  1/6 odds of removing your opponents piece or your piece and 2/3 odds of nothing happening.
4. At the start of each round pick whether you want to roll the dice or place your symbol.
5. If dice was rolled proceed with whatever attribute you were given.
6. If you chose to place you piece then place it on the board.
7. Repeat steps 4-6 until there is a draw or a winner.

Updated Instructions:
In order to play Dice Tic-Tac-Toe, you first need to install socket32.py, basegame_server.py, basegame_client1.py, and basegame_client2.py.
In order to play this game, there must be 3 split terminals running.
1. Initialize basegame_server.py in one of the terminals. 
2. Initialize basegame_client1.py in one of the other terminals.
3. Initialize basegame_client2.py in the last terminal.
4. Have the player in basegame_client1.py pick which dice they would like to use.
5. Have the player in basegame_client2.py pick which dice they would like to use.
  * Extreme Dice: 1/2 odds of removing your opponents piece or your piece
  * Intermediate Dice: 1/4 odds of removing your opponents piece or your piece and 1/2 odds of nothing happening.
  * Beginnner Dice:  1/6 odds of removing your opponents piece or your piece and 2/3 odds of nothing happening.
6. At the start of each round pick whether you want to roll the dice or place your symbol.
7. If dice was rolled proceed with whatever attribute you were given.
8. If you chose to place you piece then place it on the board.
9. Repeat steps 6-8 until there is a draw or a winner.
10. Select whether you would like to play another round.

Resources Used:
  ChatGPT: Was used to refine formatting issues (i.e. find a way to clear the terminal to avoid clutter and format text to appear more visibly clear in the terminal).
* Commented parts where ChatGPT was used.
  Server Logic:
* Pset 3 (copied socket32.py)
* Modified socket logic for 2 clients: https://www.youtube.com/watch?v=5G_bNVKdECk
* Threading logic used for 2 clients: https://docs.python.org/3/library/threading.html
