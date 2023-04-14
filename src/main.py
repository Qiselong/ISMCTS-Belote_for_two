from Cards import Card
from tools_temp import *
from game import *
import random
from Mcts import *
from ismcts_state import *
import os

os.system('clear')

random.seed(1)
g = Game('mcts', 'r', 'B')
g.generation('r')
g.sim()
