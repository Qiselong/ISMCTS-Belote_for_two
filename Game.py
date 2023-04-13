import random
import copy

# class holding the cards.
class GameState:
    def __init__(self, cards= []):
        self.numberOfPlayers = 2
        self.player = 'A'
        self.cards = cards

    def shuffle(self, cards):
        self.cards = cards

    def nextPlayer(self):
        if self.player == 'A':
            self.player = 'B'
        else:
            self.player = 'A'

    def cloneAndRandomize(self, player):
        """ randomize information not vis from the pov of player"""
        st = GameState(cards = self.cards)
        uk_cards = []   #list of uk cards
        j = 0
        idx = []        #idinces of uk cards in st.cards
        for obs in st.cards:
            if obs.isVisible == False or (obs.inHand == True and obs.player != player):
                uk_cards.append(copy.deepcopy(obs))
                idx.append(j)
            j+=1

        #uk_cards is then a list of card whose positions are unknown to player. Now we have to shuffle the values.
        uk_cards.shuffle()
        for j in range(len(idx)):
            st.cards[j].change_vals(uk_cards[j].col, uk_cards[j].val)
    
    def GetMoves(self):
        
        
