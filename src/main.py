from Cards import Card
from tools_temp import *
from game import *
import random

random.seed(1)
g = Game('r', 'h', 'B')      #create a game instance
g.generation()               #shuffle the cards
g.sim()                     #play
