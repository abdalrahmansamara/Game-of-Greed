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