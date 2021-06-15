from abc import abstractmethod
from collections import Counter
import random


class GameLogic():

    odds = {1: 1000, 2: 200, 3: 300, 4: 400, 5: 500, 6: 600}
    odds_2 = {1: 100, 5: 50}

    @staticmethod
    def calculate_score(numbers):
        dice_counter = Counter(numbers)
        score = 0
        if(len(dice_counter) == 6):
            return 1500
        if len(dice_counter) == 3 and dice_counter.most_common()[2][1] == 2:
            return 750

        for key in dice_counter:
            count = dice_counter[key]
            if(count == 3):
                score = score+GameLogic.odds[key]
            if(count == 4):
                score = score+GameLogic.odds[key]*2
            if(count == 5):
                score = score+GameLogic.odds[key]*3
            if(count == 6):
                score = score+GameLogic.odds[key]*4

            if(key == 1 or key == 5):
                if(count == 1):
                    score = score+GameLogic.odds_2[key]
                if(count == 2):
                    score = score+GameLogic.odds_2[key]*2
        return int(score)

    @staticmethod
    def roll_dice(times):
        return tuple([random.randint(1, 6) for i in range(times)])


class Banker:
    def __init__(self):
        self.balance = 0
        self.shelved = 0

    def shelf(self, value):
        self.shelved = value
        return self.shelved

    def bank(self):
        self.balance += self.shelved
        self.shelved = 0

    def clear_shelf(self):
        self.shelved = 0


class Game(Banker):
    def __init__(self, roller=None, round=1, dice=6):
        self.roller = roller
        self.round = round
        self.dice = dice
        super().__init__()
        self.flag=True



    def wlecomeing(self):
        print("Welcome to Game of Greed")
        return input("Wanna play? ")

    def handel_input_user(self):
        do_quit = input("Enter dice to keep (no spaces), or (q)uit: ")
        if do_quit == 'q':
            if(self.balance > 0):
                print(f'Total score is {self.balance} points')
            print(f'Thanks for playing. You earned {self.balance} points')
            
            self.flag=False
        else:
            self.else_if(do_quit)

    def else_if(self,do_quit):
        self.dice-=1
        round_score = GameLogic.calculate_score(tuple([int(do_quit)]))
        self.shelf(round_score)
        print(
            f'You have {self.shelved} unbanked points and {self.dice} dice remaining')
        choice = input(
            f'(r)oll again, (b)ank your points or (q)uit ')
        if (choice == 'b'):
            print(
                f'You banked {self.shelved} points in round {self.round}')
            self.bank()
            print(f'Total score is {self.balance} points')
            self.round += 1

    def rolling(self, dice):

        print(f'Rolling {dice} dice...')
        dice = self.roller(dice)
        printable_dice = ','.join([str(d) for d in dice])
        print(printable_dice)

    def play(self):
       
        user_input = self.wlecomeing()
        if user_input == 'n':
            print("OK. Maybe another time")
        else:
            while(self.flag):
                print(f'Starting round {self.round}')
                self.rolling(self.dice)                
                self.handel_input_user()
               


if __name__ == "__main__":
    roller = GameLogic.roll_dice
    game = Game(roller)
    game.play()
