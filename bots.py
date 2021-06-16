# """Place in root of Game of Greed Project,
# at same level as pyproject.toml
# """

# from abc import ABC, abstractmethod
# import builtins
# import re
# from game_of_greed.game_logic import Game
# from game_of_greed.game_logic import GameLogic


# class BaseBot(ABC):
#     """Base class for Game of Greed bots"""

#     def __init__(self, print_all=False):
#         self.last_print = ""
#         self.last_roll = []
#         self.print_all = print_all
#         self.dice_remaining = 0
#         self.unbanked_points = 0

#         self.real_print = print
#         self.real_input = input
#         builtins.print = self._mock_print
#         builtins.input = self._mock_input
#         self.total_score = 0

#     def reset(self):
#         """restores the real print and input builtin functions"""

#         builtins.print = self.real_print
#         builtins.input = self.real_input

#     def report(self, text):
#         """Prints out final score, and all other lines optionally"""

#         if self.print_all:
#             self.real_print(text)
#         elif text.startswith("Thanks for playing."):
#             score = re.sub("\D", "", text)
#             self.total_score += int(score)

#     def _mock_print(self, *args, **kwargs):
#         """steps in front of the real builtin print function"""

#         line = " ".join(args)

#         if "unbanked points" in line:

#             # parse the proper string
#             # E.g. "You have 700 unbanked points and 2 dice remaining"
#             unbanked_points_part, dice_remaining_part = line.split("unbanked points")

#             # Hold on to unbanked points and dice remaining for determining rolling vs. banking
#             self.unbanked_points = int(re.sub("\D", "", unbanked_points_part))

#             self.dice_remaining = int(re.sub("\D", "", dice_remaining_part))

#         elif line.startswith("*** "):

#             self.last_roll = [int(ch) for ch in line if ch.isdigit()]

#         else:
#             self.last_print = line

#         self.report(*args, **kwargs)

#     def _mock_input(self, *args, **kwargs):
#         """steps in front of the real builtin print function"""

#         if self.last_print == "(y)es to play or (n)o to decline":

#             return "y"

#         elif self.last_print == "Enter dice to keep, or (q)uit:":

#             return self._enter_dice()

#         elif self.last_print == "(r)oll again, (b)ank your points or (q)uit:":

#             return self._roll_bank_or_quit()

#         raise ValueError(f"Unrecognized last print {self.last_print}")

#     def _enter_dice(self):
#         """simulate user entering which dice to keep.
#         Defaults to all scoring dice"""

#         roll = GameLogic.get_scorers(self.last_roll)

#         roll_string = ""

#         for value in roll:
#             roll_string += str(value)

#         self.report("> " + roll_string)

#         return roll_string

#     @abstractmethod
#     def _roll_bank_or_quit(self):
#         """decide whether to roll the dice, bank the points, or quit"""

#         # subclass MUST implement this method
#         pass

#     @classmethod
#     def play(cls, num_games=1):
#         """Tell Bot play game a given number of times.
#         Will report average score"""

#         mega_total = 0

#         for _ in range(num_games):
#             player = cls()
#             game = Game()
#             try:
#                 game.play()
#             except SystemExit:
#                 # in game system exit is fine
#                 # because that's how they quit.
#                 pass

#             mega_total += player.total_score
#             player.reset()

#         print(
#             f"{cls.__name__}: {num_games} games played with average score of {mega_total // num_games}"
#         )


# class NervousNellie(BaseBot):
#     """NervousNellie banks the first roll always"""

#     def _roll_bank_or_quit(self):
#         return "b"

# class YourBot(BaseBot):
#     def _roll_bank_or_quit(self):
#         """your logic here"""
#         return "b"

#     def _enter_dice(self):
#         """simulate user entering which dice to keep.
#         Defaults to all scoring dice"""

#         return super()._enter_dice()


# if __name__ == "__main__":
#     num_games = 100
#     NervousNellie.play(num_games)
#     # YourBot.play(num_games)
import builtins
import re
from abc import abstractmethod

from game_of_greed.game_logic import *





class BasePlayer:
    def __init__(self):
        self.old_print = print
        self.old_input = input
        builtins.print = self._mock_print # Methods overriding
        builtins.input = self._mock_input # Methods overriding
        self.total_score = 0

    def reset(self):
        builtins.print = self.old_print
        builtins.input = self.old_input

    # The default behaviour
    @abstractmethod
    def _mock_print(self, *args):
        self.old_print(*args)

    @abstractmethod
    def _mock_input(self, *args):
        return self.old_input(*args)

    @classmethod
    def play(cls, num_games=1):

        mega_total = 0

        for i in range(num_games):
            player = cls()
            game = Game() # doesn't pass a mock roller
            try:
                game.play()
            except SystemExit:
                # in game system exit is fine
                # because that's how they quit.
                pass

            mega_total += player.total_score
            player.reset()

        print(
            f"{num_games} games (maybe) played with average score of {mega_total // num_games}"
        )


class BasicBot(BasePlayer):
    def _mock_input(self, *args):
        self.old_print(*args)
        return "n"
    def _mock_print(self, *args):
        self.old_print(*args)


class NervousNellie(BasePlayer):
    def __init__(self):
        super().__init__()
        self.roll = None

    def _mock_print(self, *args):
        first_arg = args[0]
        first_char = first_arg[0]
        if first_char.isdigit():
            self.roll = tuple(int(char) for char in first_arg.split(","))
        elif first_arg.startswith("Thanks for playing."):
            self.total_score = int(re.findall(r"\d+", first_arg)[0])
        self.old_print(first_arg)

    def _mock_input(self, *args):
        prompt = args[0]
        if prompt.startswith("Wanna play?"):
            return "y"
        elif prompt.startswith("Enter dice to keep (no spaces), or (q)uit:"):
            scorers = GameLogic.get_scorers(self.roll)
            keepers = "".join([str(ch) for ch in scorers])
            return keepers
        elif prompt.startswith("(r)oll again, (b)ank your points or (q)uit "):
            return "r"
        else:
            raise ValueError(f"Unrecognized prompt {prompt}")



if __name__ == "__main__":
    # BasicBot.play(100)
    NervousNellie.play(1)