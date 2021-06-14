# Game of greed


this is the first phase of game of greed

## functionality


up to now, we have two classes, GameLogic and Banker

GameLogic has two static methods, calculate_score: to calculate the score for the round, and roll_dice to return random numbers between 1 and 6, the amount of values in the tuple depends on the input number to the method

Banker has for methods:

1. init: for initializing an instance

2. shelf: for storing a value in a temporary position

3. bank: to save the value inside the accumulator

4. clear_shelf: to clear the temporary shelf