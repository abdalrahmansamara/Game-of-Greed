from abc import abstractmethod
from collections import Counter
import random

class GameLogic():
    @staticmethod
    def calculate_score(self,numbers):
        ctr = Counter(numbers)
        if(ctr.most_common(1)[0][1] == 1):
            return 1500
        elif(ctr.most_common()[0][1] == 2 and ctr.most_common()[1][1] == 2 and ctr.most_common()[2][1] == 2):
            return 1500
        elif (ctr.most_common()[0][1] == 3 and ctr.most_common()[1][1] == 3):
            return 1200
        
    @staticmethod 
    def roll_dice(times):
        return tuple([random.randint(1,6) for i in range(times)])

class Banker:
    def __init__(self) :
        self.balance=0
        self.shelved=0


    def shelf(self ,value):
       self.shelved=value
       return self.shelved  

    def bank (self):
        self.balance +=self.shelved
        self.shelved=0


    def clear_shelf(self):
         self.shelved=0