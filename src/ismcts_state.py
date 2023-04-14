from tools_temp import *

class State():
    def __init__(self, cards=[],p='A',pts=[0,0], attack = -1 ):
        self.cards = cards      #cards state (list of len 32)
        self.attack = attack    #potential attack card
        self.points = pts       #
        self.player = p         #player that will move
    

    def CloneAndRandomize(self):
        """randomize the information unknown to self.player."""
        # note that we dont have to specify which player do this, as this is always self.player: indeed this function is only called at the root which is exactly when the mcts player is self.player.
        st = copy.deepcopy(self)
        st.cards = determinization(st.cards, st.player)
        #print(st.player)
        #print_game(st.cards, mode = 'B',cls = False)
        return st

    def GetMoves(self):
        """ return a list of cards corresponding to legal moves"""
        return can_play(self.cards, self.player, self.attack)

    def nextPlayer(self):
        if self.player == 'A':
            self.player = 'B'
        else:
            self.player = 'A'

    def DoMove(self, card):
        """ change the state of game according to the play of card, aka change card status, player, points, and attack . """
        #print(f"play {card.name()}")

        #1. change card status
        for obs in self.cards: #find the card that is played and make it unplayble
            if obs == card:
                obs.isPlayed = True
                obs.isPlayable = False
                break
        self.cards = update(self.cards, card) #potentially unveil a card

        #2. determine who plays next
        if self.attack != -1:
            if card.beat(self.attack): #then we beat the attacking card aka. the player do not change.
                self.player = self.player
            else:
                self.nextPlayer()
        else:
            self.nextPlayer()

        #3. computes points (not useful beyond the simulation.)
        if self.attack != -1:
            #notice the winner of the round is self.player as we already did the update.
            pts_earned = self.attack.points() + card.points()
            if self.player == 'A':
                self.points[0] += pts_earned
            else:
                self.points[1] += pts_earned


        #4. change attack card status 
        if self.attack != -1:
            self.attack = -1
        else:
            self.attack = card
    
    def GetResult(self, player):
        if player == 'A':
            return self.points[0]
        else:
            return self.points[1]
    