from Cards import Card
from tools_temp import *
from game import *
import random
from Mcts import *
from ismcts_state import *
import os
import time
import platform

if platform.system() == 'Linux':
    os.system('clear')
elif platform.system() == 'Darwin':
            # Mac
    os.system('cls') #TODO: verify this actually works?
elif platform.system() == 'Windows':
    os.system('cls')


print("Thanks for participating in this experiment !\nThis particular scripts aims at teaching you the rules of the game. You can replay it as much time as you want if something is not clear.\nType enter to continue ")
x = input()

random.seed(1)
g = Game('r', 'h', 'A')
g.generation()


g.print()

print("This is the game board. You are player B.\n You and your opponent have 6 cards in hands, and 10 cards on the board each. cards values range from [7, 8, .. King, Ace].\nColors are the classics: [Clubs, Diamonds, Hearts, Spade]\nType enter to continue")
x = input()

g.print()
print("Some cards on the board are visible to both players (VISI) and some are invisible for the moment (INVI).\nWhen a VISI card is played, the card under it, if it exists is revealed to both player and moves to the VISI part of the board.\nCards in HAND are only visible to the player owning them.\nWhen you have to play a card, you can only play that is on your side of the board and you can see. ??? denotes a card you cannot see because it is hidden or in the hand of your opponent.\nType enter to continue")
x = input()

g.print()
print("The game goes in 16 tricks. The attacking player plays one of his cards, and the defender plays one of his own according to the rules.\nThe winner of the trick becomes the attacking player for the next trick.\nType enter to continue")
x = input()


g.print()
print("The color of the attacking card is the dominant color of the trick. The defending player must play a card of the same color if he owns one.\nIf they does not, they must play a trump card. They can play any card otherwise.\nTrump cards are Clubs card in this program. Trump cards always win against other colors.\nWhen the dominant color is trump, the defending player must play a stronger trump, otherwise a trump, otherwise anything else.\n\nOrder of strength:\nNon-trump : A > 10 > K > Q > J > 9 > 8 > 7 \nTrump     : J > 9 > A > 10 > K > Q > 8 > 7\n\nTo remember easily, just note that the trump order is the same but with J and 9 shifted as best cards.\nPlease also note that 10 is unusually stronger than figures.\nType enter to continue")
x = input()

g.print()
print("The next time you type enter, the opponent will play a card of his hand, AD.\nYou have exactly one Diamond card: JD, so you will be forced to play it.\nA prompt will appear on the screen, you will have to press the number associated to JD (0) and enter to play it. ")
x = input()

g.round()

g.print()
print("As Diamond is not the trump color and A > J, A wins the trick as well as 13 points. The points distribution is the following:")

print("\nNon-trump : A > 10 > K > Q > J > 9 > 8 > 7")
print("            11  10   4   3   2   0   0   0")      
print("Trump     : J > 9 > A > 10 > K > Q > 8 > 7")
print("            20  14  11  10   4   3   0   0 ")

print("\nMaking a grand total of 162 points, including the 10 bonus points to the winner of the 16th trick.\n On the first trick, your opponent earned 11 + 2 = 13 points.")
print("\nNote that below the board, you can see the current score and a detail round by round of what happened.\nIn particular, you can see if cards has been revealed from INVI to VISI. Now, QD is available for you to play in future tricks.")
print("\nNow the game will play the tricks until all cards are played. Try to score the maximum number of points.\nType enter to continue")
x = input()

for k in range(15):
    g.round()

print(f'Final score: {g.points[0]} to {g.points[1]}.')
if g.points[0] > g.points[1]:
    print(f'Player A wins')
elif g.points[0] < g.points[1]:
    print(f'You win ! Congratulations. ')
else:
    print('Draw ! No one wins.')

print("If you feel comfortable with the rules yet, you can try to beat the MCTS player by running main.py. If you need a remainder of the rules/relative strength of cards/points you can find the text that was displayed in this terminal in the file tutorial.txt.")