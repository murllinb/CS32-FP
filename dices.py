import random

class StandardDice:
    name = "Standard Dice"
    description = "Rolls a number from 1 to 6 with equal probability."

    def roll(self):
        return random.randint(1, 6)


class BinaryDice:
    name = "Binary Dice"
    description = "50/50 chance of rolling either a 1 or a 6."

    def roll(self):
        return random.choice([1, 6])


DICE_OPTIONS = {
    "1": StandardDice,
    "2": BinaryDice,
}

def choose_dice(player):
    print(f"\n  Player {player}, choose your dice:")
    for key, cls in DICE_OPTIONS.items():
        print(f"    {key}. {cls.name} — {cls.description}")
    while True:
        choice = input("  Enter 1 or 2: ").strip()
        if choice in DICE_OPTIONS:
            dice = DICE_OPTIONS[choice]()
            print(f"  Player {player} is using the {dice.name}!")
            return dice
        print("  Invalid choice. Please enter 1 or 2.")
