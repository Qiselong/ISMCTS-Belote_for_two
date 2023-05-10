import random
from Cards import Card
import os
from tools_temp import *
from Mcts import *
from ismcts_state import *

itermax = 500
return_hist_winner = True


global hist_winner
hist_winner = []

class Game:

    def __init__(self,A, B, pinit, view = 'B'):
        '''A \in {'r', 'mcts'}, B \in {'h', 'mcts', 'r'}'''
        hist_winner = []
        self.stratA = A  #Note: A can not be a human player.
        self.stratB = B #Note: B is either a human or an AI.
        self.roundID = 1
        self.points = [0,0]
        self.cards = []
        self.history = '' # string containing all the informations of the previous rounds.
        self.state = None
        self.view = view #printing method
        if pinit == 'r': #initial player
            self.player = random.choice(['A', 'B'])
        else: self.player = pinit 

    def generation(self, method = 'r'):
        ''' generate a shuffle of all the cards, and initialize a gamestate. 'r' -> all random '''
        if method == 'r':
            self.cards = random_shuffle()
        self.state = State(self.cards, self.player)

    def print(self):
        ''' print the game. 'B' -> from the pov of B. Other mode: 'omni' -> see all.'''
        print_game(self.cards, self.view)
        print(f"Points: A:{self.points[0]}, B: {self.points[1]}")
        print(self.history)
    
    def play_a_card(self, player, attack = -1, exp = 100):
        ''' Returns a card of player according to a potential attack card.'''
        av = can_play(self.cards, self.player,attack)

        def choice_strat(av, strat, state = -1):
            '''choice of cards according to some strategy. 'r' = random 'h' = human'''
            if strat == 'r':
                c = random.choice(av)
                self.state.DoMove(c)
                return c
            if strat == 'h':
                c = card_choice(av)
                self.state.DoMove(c)
                return c
            if strat == 'mcts':
                #print(f'mcts plays. Player:{self.player} , available cards {[obs.name() for obs in av]}')
                a = ISMCTS(self.state, itermax, exp = exp)
                self.state.DoMove(a)
                #print(f'move chose {a.name()}')
                return a
        if self.player == 'A':
            return choice_strat(av, self.stratA)
        else:
            return choice_strat(av, self.stratB)


    def next_player(self):
        if self.player == 'A': 
            self.player = 'B'
        elif self.player == 'B':
            self.player = 'A'

    def round(self, exp = 0.7):#, id):
        ''' given the winner of the last round, simulate a round. returns the winner of the round and updates the history.'''
        #print(self.history)
        self.history += f'R {self.roundID} : '
        if self.player == 'B' and self.stratB == 'h':
            print_game(self.cards)
            print(self.history)
        attack = self.play_a_card(self.player, exp = exp)
        self.cards = play(self.cards, attack)
        self.play_hist(attack)                      #hist update after each play

        self.next_player()
        #print(f'player changed to {self.player} after the other played {attack.name()}!')

        if self.player == 'B' and self.stratB == 'h':
            #clear screen + print history
            print_game(self.cards)
            print(self.history)
        defense = self.play_a_card(self.player, attack, exp=exp)
        self.cards = play(self.cards, defense)
        self.play_hist(defense)                     #hist update after each play
        self.player = self.round_hist(attack, defense)   #hist update: end of round + update for round winner
        self.roundID += 1
        hist_winner.append(self.player)

    def play_hist(self,c):
        '''update the history when p plays c. (eventually revealing cards etc.), eol: if true then adds and endofline char after appending the history. '''
        p = c.player
        h = f'{p}: [{c.name()}'
        d=f']. '
        for obs in self.cards:
            #print(f'played {c.name()}, obs {obs.name()}')
            if obs.position == c.position and obs.player == c.player and obs != c and obs.isPlayed == False and obs.inHand == False:
                d=f'; {obs.name()} revealed]. '
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


    def sim(self, verbose = True,exp = 0.7):
        '''play all the round after one another.'''
        for i in range(16):
            self.round(exp)
            #print(len(hist_winner))
            #print_game(self.cards, cls = False)
        if verbose: print(f'{self.player} earns 10 bonus points for last trick.')
        if self.player == 'B':
            self.points[1] += 10
        else: self.points[0] += 10
        if self.points[0]>self.points[1]:
            winner = 'A'
        elif self.points[0] == 81:
            winner = 'None'
        else: winner = 'B'
        if verbose: print(f'winner: {winner}, final score: {self.points}')
        if return_hist_winner:
            return hist_winner



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
            #print_game(game)
            #print(history)
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
    #print(gA, gB)
