import random

class Card:
    def __init__(self, col, val, p, inH, playable, pos, isVis) :
        self.col = col
        self.val = val
        self.player = p
        self.inHand = inH
        self.isPlayable = playable
        self.position = pos
        self.isVisible = isVis
        self.isPlayed = False


    def points(self):
        pts_trump = [20,14,11, 10, 4, 3, 0, 0]
        pts = [11, 10, 4, 3, 2, 0, 0, 0]
        if self.col == 0:
            return pts_trump[self.val]
        else:
            return pts[self.val] 
            
    def name(self):
        """return the name of a card as a string of 3 char"""
        col_name = ['C', 'D', 'H', 'S']
        trump_name = [' J', ' 9', ' A', '10', ' K', ' Q', ' 8', ' 7']
        nontrump_name = [ ' A', '10', ' K', ' Q', ' J', ' 9', ' 8', ' 7']
        nm =''
        if self.col == 0:
            nm+= trump_name[self.val]
        else:
            nm+= nontrump_name[self.val] 
        return nm+col_name[self.col]
            
    def beat(self, attack): 
        """ determine if self beats an attacking card"""
        if attack.col == self.col:
            return self.val < attack.val
        elif self.col == 0:
            return True
        else: 
            return False
    
            
    def unveiled(self, player):
        """determine is a card is unknowned to a given player"""
        if self.isVisible == False or (self.player != player and self.inHand == True):
            return True
        else: 
            return False

    def play(self):
        """ play a card."""
        self.isPlayed = True
        #self.position = -1

            
    def set_player(self,player):
        self.player = player

    def set_inHand(self,x):
        self.inHand(x)

    def set_col(self,col):
        self.col = col

    def set_val(self,val):
        self.val = val
        
    def set_isPlayable(self,p):
        self.isPlayable = p
        
    def set_position(self,x):
        self.position=x
        
    def set_isVisible(self,y):
        self.isVisible = y
        
        
