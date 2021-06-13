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