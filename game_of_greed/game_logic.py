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
    
    @staticmethod
    def get_scorers(dice):
        # version_3

        all_dice_score = GameLogic.calculate_score(dice)

        if all_dice_score == 0:
            return tuple()

        scorers = []

        for i in range(len(dice)):
            sub_roll = dice[:i] + dice[i + 1 :]
            sub_score = GameLogic.calculate_score(sub_roll)

            if sub_score != all_dice_score:
                scorers.append(dice[i])

        return tuple(scorers)


class Banker:
    def __init__(self):
        self.balance = 0
        self.shelved = 0

    def shelf(self, value):
        self.shelved += value
        return self.shelved

    def bank(self):
        self.balance += self.shelved
        self.shelved = 0

    def clear_shelf(self):
        self.shelved = 0


class Game(Banker):
    def __init__(self, roller=None, round=1, dice=6):
        self.roller = roller or GameLogic.roll_dice
        self.round = round
        self.dice = dice
        super().__init__()
        self.flag=True
        self.round_flag = True
        self.hot=False
        # self.special = False
    
    def Zilch(self):
        print('Zilch!!! Round over')
        print(f'You banked 0 points in round {self.round}')
        print(f'Total score is {self.balance} points')
        self.clear_shelf()
    
    def checking_user_input(self,current_dice,do_quit):
        tu2 = [int(i) for i in do_quit]
        un = set(tu2)
        flag = True
        for i in un:
            if current_dice.count(i) < tu2.count(i):
                flag = False
        return flag

    def welcoming(self):
        print("Welcome to Game of Greed")
        return input("Wanna play? ")
    
    def handel_input_user(self):
        [answer,current_dice] = self.rolling(self.dice)
        if (not answer):
            return
        do_quit = input("Enter dice to keep (no spaces), or (q)uit: ")
        if do_quit == 'q':
            # if(self.balance > 0):
            print(f'Total score is {self.balance} points')
            print(f'Thanks for playing. You earned {self.balance} points')
            # self.round_flag = False
            self.flag=False
            self.round_flag = False
            return
            # not sure about this, it has no need
        else:
            while not self.checking_user_input(current_dice,do_quit):
                print('Cheater!!! Or possibly made a typo...')
                printable_dice = ','.join([str(d) for d in current_dice])
                print(printable_dice)
                do_quit = input("Enter dice to keep (no spaces), or (q)uit: ")
            self.else_if(do_quit)

    def else_if(self,do_quit): # assuming the user is honest for now
        while(self.round_flag):
            # get proper tuple out of the input
            future_tuple = []
            for num in do_quit:
                future_tuple.append(int(num))
            t = tuple(future_tuple)
            self.dice -= len(t)
            # end of tuple the input

            
           
            
            round_score = GameLogic.calculate_score(t)

            self.shelf(round_score)
            print(
                f'You have {self.shelved} unbanked points and {self.dice} dice remaining')
            choice = input(
                f'(r)oll again, (b)ank your points or (q)uit ')
            if len(Counter(t)) == 3 and Counter(t).most_common()[2][1] == 2:
                self.dice=6
                # self.special = True
            if (choice == 'b'):
                print(
                    f'You banked {self.shelved} points in round {self.round}')
                self.bank()
                print(f'Total score is {self.balance} points')
                self.round += 1
                self.round_flag = False
            # no provided info about q in choice
            elif choice == 'q':
                self.flag = False
                self.round_flag = False
                print(f'Total score is {self.balance} points')
                print(f'Thanks for playing. You earned {self.balance} points')
                # print('why quitting')
                return
            elif choice == 'r':
                if self.dice == 0:
                    self.flag=False
                    self.round_flag = False
                    return
                # self.shelf(round_score)
                self.handel_input_user()


    def rolling(self, dice):

        print(f'Rolling {dice} dice...')
        dice = self.roller(dice)
        printable_dice = ','.join([str(d) for d in dice])
        print(printable_dice)
        zl = GameLogic.calculate_score(dice)
        if zl == 0:
            self.Zilch()
            self.round_flag = False
            self.round += 1
            return [False,dice]
        else:
            return [True,dice]

    def play(self):
       
        user_input = self.welcoming()
        if user_input == 'n':
            print("OK. Maybe another time")
        else:
            while(self.flag and self.round <= 20):
                print(f'Starting round {self.round}')
                self.round_flag = True
                self.dice = 6
                self.handel_input_user()
            else:
                print(f'Thanks for playing. You earned {self.balance} points')
               

# main
if __name__ == "__main__":
    roller = GameLogic.roll_dice
    game = Game(roller)
    game.play()
