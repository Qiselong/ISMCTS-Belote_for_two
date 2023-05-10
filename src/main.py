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


#for k in range(300):
    hist_winner = []
    t0 = time.time()
    #UI
    os.system('clear')
    f = open('logsB.txt','a')
    print(f'Game n°{k+1}. Current avg scores: {pts[0]//max(k,1)} (r) to {pts[1]//max(k,1)} (mcts); avg_time {TTime/(max(k,1))}')
  
    #Simulation
    g = Game('r', 'mcts', 'r')
    g.generation('r')
    hist_winnerz = g.sim(False)[-16:]
    print(len(hist_winnerz))
    t1 = time.time()

    #post treatement
    pts[0] += g.points[0]
    pts[1] += g.points[1]
    f.write(str(g.points[0])+';'+ str(g.points[1])+';'+listTostr(hist_winnerz) +'\n')

    TTime += t1-t0
    appendA(hist_winnerz)
    appendB(hist_winnerz)
    
#print(winner_A)
#print(winner_B)



g = Game('mcts', 'h', 'B')
g.generation()
g.sim()

#print_game(g.cards, mode = 'omni')