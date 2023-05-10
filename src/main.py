from Cards import Card
from tools_temp import *
from game import *
import random
from Mcts import *
from ismcts_state import *
import os
import time

os.system('clear')

winner_A = [0 for i in range(16)]
winner_B = [0 for i in range(16)]

pts = [0,0]

avg_time = 0
TTime = 0

def appendA(hist):
    for i in range(len(hist)):
        if hist[i] == 'A':
            winner_A[i] += 1
def appendB(hist):
    for i in range(len(hist)):
        if hist[i] == 'B':
            winner_B[i] += 1
def listTostr(L):
    l = ''
    for i in L:
        l+=str(i)
    return l

play_again = True

while play_again:

    g = Game('mcts', 'h', 'r')
    cards = g.generation('f')
#tA, pA, tB = 0,0,0
#for c in cards:
    #tA += (c.col== 0) and (c.player == 'A')
   # tB += c.col == 0 and c.player == 'B'
  #  pA += (c.player == 'A')*c.points()
 #   print(c.name(), c.player)
#print(tA, tB, pA)
#x = input()
    fst_player = '' # records 
    fst_player += g.player

    for i in range(16):
    
        g.round()
        fst_player+=g.player
    if g.player == 'A':
        g.points[0]+=10
    else:
        g.points[1] += 10
    print(f'Final score:{g.points[0]} to {g.points[1]}')
    if g.points[1] > g.points[1]:
        print("Congratulations !")
    else:
        print("", end ="")
        #print("XD ! You are so bad!! Note that I'm writing this without having played myself agaisnt the ISMCTS, so i'm probably also bad.")

    f = open('../logs.txt', 'a')
    f.write(fst_player+';'+str(g.points[0])+'\n')
    f.close()
    print('\n\n')
    x = input('type enter to play again')
    play_again = (x == '')

#print_game(g.cards, mode = 'omni')