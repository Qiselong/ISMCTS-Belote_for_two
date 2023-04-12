##

class Node():
    def __init__(self, p, a, move=None, parent = None):
        self.move = None        #what has been done from parent node
        self.player = p         #who's player is playing?
        self.attack = a         #is it an attack decision we are doing?
        self.parent = parent    #parent node adress
        self.pts = 0            #sum of rewards of leaves
        self.pts2 = 0           #sum of rewards **2
        self.children = []      #list of children
        self.visits = 0         #visits
        self.avail = 0          #visits of valid siblings
        
