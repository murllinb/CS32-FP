# CS32-FP
CS32 FP by [Murllin Bender,  Elisabeth Lai, Siya Patel]

Our project is a take on the infamous Tic-Tac-Toe game. This game "Dice Tic-Tac-Toe" can have two players alternating between turns, laying down X's and O's on a 3x3 9 piece board. After they get three in a row, they win! --- Unlike normal Tic-Tac-Toe, this take has unique dices with powerups that the player can choose from. Theres three different dices that users can choose like characters --- and they have unique attributes. When its a player's turn, they can choose whether or not to roll it or play like normal. These dices will keep the game unique and interesting. We have a an overall game system where scores and streaks are tracked across rounds. Additionally, there is a shop system where users can buy items with the coins they earn after every round. Lastly, our new feauture we implemented is Turtle, a drawing system that sketches out the board.

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


Resources Used:
  ChatGPT: Was used to refine formatting issues (i.e. find a way to clear the terminal to avoid clutter and format text to appear more visibly clear in the terminal).
* Commented parts where ChatGPT was used.
  Server Logic:
* Pset 3 (copied logic from socket)
* Modified socket logic for 2 clients: https://www.youtube.com/watch?v=5G_bNVKdECk
* Threading logic used for 2 clients: https://docs.python.org/3/library/threading.html
