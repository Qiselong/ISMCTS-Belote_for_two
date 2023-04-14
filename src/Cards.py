import random

class Card:
    def __init__(self, col, val, p, inH, playable, pos, isVis) :
        self.col = col              # color
        self.val = val              # strength
        self.player = p             # player owning the card
        self.inHand = inH           # if the card is in the hand of the player
        self.isPlayable = playable  # == inHand or visible
        self.position = pos         # = -1 if inHand or 0,4.
        self.isVisible = isVis      # if pos >-1. False => theres a card with same position but visible.
        self.isPlayed = False       # we are done with this card.


    def points(self):
        pts_trump = [20,14,11, 10, 4, 3, 0, 0]
        pts = [11, 10, 4, 3, 2, 0, 0, 0]
        if self.col == 0:
            return pts_trump[self.val]
        else:
            return pts[self.val] 
        
    def change_vals(self, col, val):
        #useful later to change the card id while keeping its other properties
        self.col = col
        self.val = val
            
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
    
    def unveil(self, card):
        """ when card is played, if card has the same pos as self, change the status of self as visible. 
        Note that card's status 'played' is change elsewhere."""
        if self.position == card.position and card.player == self.player:
            self.isVisible = True
            self.isPlayable = True

    def __eq__(self, other):
        if type(other) == int:
            return False
        return self.col == other.col and self.val == other.val
    
    def visBy(self, player):
        return self.isPlayed == True or self.isVisible or (self.inHand and self.player == player) 


        
        
