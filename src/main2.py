from Cards import Card
from tools_temp import *
from game import *
import random
from Mcts import *
from ismcts_state import *
import os
import time
from golden_section import *
from pprint import pprint
os.system('clear')

global dic
dic = {}



def simulate_games(x,k= 200, msg = ''):
    """ simulate k games of random vs mcts player. x: exp factor. Return the number of avg points earned by the mcts player."""
    pts = [0,0]
    random.seed(1)
    for i in range(k):
        os.system('clear')
        pprint(dic)
        print(f'evaluation f({x}), {i}/{k}; {pts[1]//max(1, i)}')
        g = Game('r', 'mcts', 'r')
        g.generation('r')
        g.sim(False, exp = x)
        pts[1] += g.points[1]
        
    return pts[1]/k

def f(x, k = 50):
    x = int(x*1000)/1000
    if x in dic:
        return 162 - dic[x]
    else: 
        y = simulate_games(x, k)
        dic[x] = y
        return 162-y # as we look for a minimum.

#gss(f, 0, 300, tol = 0.1)

simulate_games(212, 1000)








#print_game(g.cards, mode = 'omni')