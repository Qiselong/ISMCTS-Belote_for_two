import random
from Cards import Card
import os
from tools_temp import *




class Game:

    def __init__(self,A, B, pinit):
        self.stratA = A  #Note: A can not be a human player.
        self.stratB = B #Note: B is either a human or an AI.
        self.roundID = 1
        self.points = [0,0]
        self.cards = []
        self.history = '' # string containing all the informations of the previous rounds.
        if pinit == 'r': #initial player
            self.player = random.choice(['A', 'B'])
        else: self.player = pinit 

    def generation(self, method = 'r'):
        ''' generate a shuffle of all the cards. 'r' -> all random '''
        if method == 'r':
            self.cards = random_shuffle()

    def print(self, method = 'B'):
        ''' print the game. 'B' -> from the pov of B. Other mode: 'omni' -> see all.'''
        print_game(self.cards, method)
        print(f"Points: A:{self.points[0]}, B: {self.points[1]}")
        print(self.history)
    
    def play_a_card(self, player, attack = -1):
        ''' Returns a card of player according to a potential attack card.'''
        av = can_play(self.cards, player,attack)

        def choice_strat(av, strat):
            '''choice of cards according to some strategy. 'r' = random 'h' = human'''
            if strat == 'r':
                return random.choice(av)
            if strat == 'h':
                c = card_choice(av)
                return c 
        
        if self.player == 'A':
            return choice_strat(av, self.stratA)
        else:
            return choice_strat(av, self.stratB)


    def next_player(self):
        if self.player == 'A': 
            self.player = 'B'
        else:
            self.player = 'A'

    def round(self):#, id):
        ''' given the winner of the last round, simulate a round. returns the winner of the round and updates the history.'''
        self.history += f'R {self.roundID} : '
        if self.player == 'B':
            print_game(self.cards)
            print(self.history)
        attack = self.play_a_card(self.player)
        self.cards = play(self.cards, attack)
        self.play_hist(attack)                      #hist update after each play

        self.next_player()

        if self.player == 'B':
            #clear screen + print history
            print_game(self.cards)
            print(self.history)
        defense = self.play_a_card(self.player, attack)
        self.cards = play(self.cards, defense)
        self.play_hist(defense)                     #hist update after each play
        self.player = self.round_hist(attack, defense)   #hist update: end of round + update for round winner
        self.roundID += 1

    def play_hist(self,c):
        '''update the history when p plays c. (eventually revealing cards etc.), eol: if true then adds and endofline char after appending the history. '''
        p = c.player
        h = f'{p}: {c.name()}'
        
        for obs in self.cards:
            d=f'. '
            print(f'played {c.name()}, obs {obs.name()}')
            if obs.position == c.position and obs.player == c.player and obs != c:
                d=f', revealing card f{obs.name()}. '
        self.history+=h
        self.history+=d
        

    def round_hist(self, attack, defense):
        ''' result of the round + append history with the on going scores. '''
        winner = attack.player
        if defense.beat(attack):
            winner = defense.player
        self.update_score(winner, attack, defense)
        h = f'{winner} wins {defense.points() + attack.points()} pts. Score: {self.points}\n'
        self.history += h
        return winner
    
    def update_score(self, winner, attack, defense):
        pts = attack.points() + defense.points()
        if winner == 'A':
            self.points[0] += pts
        else: self.points[1] += pts


    def sim(self):
        for i in range(16):
            self.round()
        print(f'{self.player} earns 10 bonus points for last trick.')
        if self.player == 'B':
            self.points[1] += 10
        else: self.points[0] += 10
        if self.points[0]>self.points[1]:
            winner = 'A'
        elif self.points[0] == 81:
            winner = 'None'
        else: winner = 'B'
        print(f'winner: {winner}, final score: {self.points}')

random.seed(1)
g = Game('r', 'h', 'B')      #create a game instance
g.generation()               #shuffle the cards
g.sim()                     #play



def random_game():
    """play a game against a random adversary. may be useless later."""
    random.seed(1)
    
    #points initialization
    gA = 0
    gB = 0
    game = random_shuffle()
    winner = 'B'#random.choice(['A', 'B'])
    history = ''
    for round in range(1,17):
        os.system('clear')
        history+='\nROUND '+str(round) +' # '
        if winner == 'A':
            attack = random.choice(can_play(game, 'A'))
            #rc is a random card chosen from the cards A can play.
        
            game = play(game, attack)
            #game = update(game,attack)
            history+='A plays '+attack.name()+ ' # '
            print_game(game)
            print(history)
            playable_B = can_play(game, 'B', attack)
            defense = card_choice(playable_B)
            #defense.play()
            game = play(game, defense)
            #game = update(game, defense)
            history+= 'B plays ' + defense.name()+ ' # '

            if defense.beat(attack):
                winner = 'B'
                gB += attack.points()+ defense.points()
                history +=  winner +' wins ' + str(attack.points()+defense.points())+ 'points. ## '
            else: #else A wins again.
                winner = 'A'
                gA += attack.points() + defense.points()
                history += winner +' wins '+str(attack.points()+defense.points())+ 'points.' + ' ## '

        elif winner == 'B':
            print_game(game)
            print(history)
            playable_B = can_play(game, 'B')
            attack = card_choice(playable_B)
            #attack.play()
            game = play(game, attack)
            game = update(game, attack)
            history+= 'B plays ' + attack.name() + ' # '

            defense_possible = can_play(game, 'A', attack)
            defense = random.choice(defense_possible)
            #defense.play()
            game = play(game, defense)
            history+='A plays '+defense.name()+ ' # '
            #game = update(game, defense)
            if defense.beat(attack):
                winner = 'A'
                gA += attack.points()+ defense.points()
                history +=  winner +' wins '+str(attack.points()+defense.points())+ 'points.' + ' ## '

            else: #else B wins again.
                winner = 'B'
                gB += attack.points() + defense.points()
                history +=  winner +' wins ' + str(attack.points()+defense.points())+ ' points ## '
        history += 'Total points A: ' + str(gA)+'; B:' + str(gB)
    if winner == 'A':
        gA += 10
    else: 
        gB += 10
    print(gA, gB)
