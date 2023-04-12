import random
from Cards import Card
import os

def random_game():
    """play a game against a random adversary."""
    random.seed(1)
    
    #points initialization
    gA = 0
    gB = 0
    game = random_shuffle()
    winner = 'B'#random.choice(['A', 'B'])
    history = ''
    for round in range(1,17):
        os.system('clear')
        history+='\nROUND '+str(round) +'\n'
        if winner == 'A':
            attack = random.choice(can_play(game, 'A'))
            #rc is a random card chosen from the cards A can play.
        
            attack.play()
            game = update(game,attack)
            history+='A plays '+attack.name()
            print_game(game)
            print(history)
            playable_B = can_play(game, 'B', attack)
            defense = card_choice(playable_B)
            defense.play()
            game = update(game, defense)
            history+= '\nB plays ' + defense.name()

            if defense.beat(attack):
                winner = 'B'
                gB += attack.points()+ defense.points()
                history += '\nPlayer ' + winner +' wins. Points earned: ' + str(attack.points()+defense.points())
            else: #else A wins again.
                winner = 'A'
                gA += attack.points() + defense.points()
                history += '\n'+ winner +' wins '+str(attack.points()+defense.points())+ 'points.' 

        if winner == 'B':
            print_game(game)
            print(history)
            playable_B = can_play(game, 'B')
            attack = card_choice(playable_B)
            attack.play()
            game = update(game, attack)
            history+= '\nB plays ' + attack.name()

            defense_possible = can_play(game, 'A', attack)
            defense = random.choice(defense_possible)
            defense.play()
            history+='\nA plays '+defense.name()
            game = update(game, defense)
            if defense.beat(attack):
                winner = 'A'
                gA += attack.points()+ defense.points()
                history += '\n'+ winner +' wins '+str(attack.points()+defense.points())+ 'points.' 

            else: #else B wins again.
                winner = 'B'
                gA += attack.points() + defense.points()
                history += '\nPlayer'+ winner +'. Points earned: ' + str(attack.points()+defense.points())
    if winner == 'A':
        gA += 10
    else: 
        gB += 10
    print(gA, gB)

def card_choice(av):
    """ display the card choice that are possible to play and take an input from the user."""
    for c in av:
        print(c.name(), end=' ')
    print('\n', end = '')
    it = 0
    for c in av:
        print(' ' + str(it), end = '  ')
        it += 1
    x = int(input('\ncard choice: '))
    return av[x]

def update(game, c):
    ''' if c is a card from the visible board, update the status of the card under it.'''
    if c.inHand == False and c.isVisible == True:
        for obs in game:
            if obs.position == c.position and obs.player == c.player and obs.isVisible == False and obs.isPlayed == False:
                obs.isVisible = True
    return game
    


def random_shuffle():
    """ return a full game aka a list of 32 Cards instance."""
    av = [(i,j) for i in range(4) for j in range(8)]
    game = []
    for i in range(6): # hand first 
        for p in ['A','B']:
            id = random.choice(av)
            c = Card(id[0],id[1], p, True, True, -1, False)
            game.append(c)
            av.remove(id)
        # Then the piles
    for p in ['A', 'B']:            #player
        for i in [True, False]:     #face up/face down
            for pos in range(5):    #position
                id = random.choice(av)
                av.remove(id)
                c = Card(id[0], id[1], p, False, i, pos, i)
                game.append(c)
    return game

def can_play(game, player,  attack = -1):
    """ return the list of playable cards. attack = -1 means we attack"""
    av_cards = [c for c in game if c.isPlayable == True and c.player == player and c.isPlayed == False] #list of cards that I possibly can play
    if attack == -1:
        return av_cards
    else:
        # if attack is trump I must play a stronger trump, or a trump if I have, or anything.
        if attack.col == 0:
            myTrump = [c for c in av_cards if c.col == 0]
            mySTrump = [c for c in myTrump if c.val < attack.val ]
            if len(mySTrump)>0:
                return mySTrump
            elif len(myTrump)>0:
                return myTrump
            else:
                return av_cards
        # if attack is not a trump i must play a card of same color
        if len([1 for c in av_cards if c.col == attack.col]) > 0:
            return [c for c in av_cards if c.col == attack.col]
        # or a trump
        elif len([1 for c in av_cards if c.col == 0]):
            return [c for c in av_cards if c.col == 0]
        # or av_cards
        else: return av_cards

def print_game(game, mode = 'B'):
    """ print the state of a game. omni : see all, B: from the pov of player B. """
    if mode == 'omni':
        print("##################")
        print("A")
        print("HAND ", end = '')
        for c in game:
            if c.player == 'A' and c.inHand == True and c.isPlayed == False:
                print(c.name(), end = ' ')
        print('\nVISI ', end = '')
        for p in range(5):
            for c in game:
                if c.player == 'A' and c.inHand == False and c.isVisible == True and c.position == p:
                    print(c.name(), end = ' ')
        print('\nINVI ', end ='')
        for p in range(5):
            for c in game:
                if c.player == 'A' and c.inHand == False and c.isVisible == False and c.position == p:
                    print(c.name(), end = ' ')

        print('\n\nB') 
        print('VISI ', end = '')
        for p in range(5):
            for c in game:
                if c.player == 'B' and c.inHand == False and c.isVisible == True and c.position == p:
                    print(c.name(), end = ' ')
        print('\nINVI ', end ='')
        for p in range(5):
            for c in game:
                if c.player == 'B' and c.inHand == False and c.isVisible == False and c.position == p:
                    print(c.name(), end = ' ')
        print("\nHAND ", end = '')
        for c in game:
            if c.player == 'B' and c.inHand == True and c.isPlayed == False:
                print(c.name(), end = ' ')
    elif mode  == 'B':
        # print according to what B knows
        print("##################")
        print("A")
        print("HAND ", end = '')    
        for c in game:
            if c.player == 'A' and c.inHand==True and c.isPlayed == False:
                print('???', end = ' ')
        print("\nVISI ", end = '')
        for pos in range(5):
            string = '   '
            for c in game:
                if c.player == 'A' and c.inHand == False and c.isVisible == True and c.position == pos:
                    string = c.name()
            print(string, end = ' ')
        print("\nINVI ", end = '')
        for pos in range(5):
            string = '   '
            for c in game:
                if c.player == 'A' and c.inHand == False and c.isVisible == False and c.position == pos:
                    string = '???'
            print(string, end = ' ')

        print('\nB')
        print('VISI ', end = '')
        for pos in range(5):
            string = '   '
            for c in game:
                if c.player == 'B' and c.inHand == False and c.isVisible == True and c.position == pos:
                    string = c.name()
            print(string, end = ' ')
        print("\nINVI ", end = '')
        for pos in range(5):
            string = '   '
            for c in game:
                if c.player == 'B' and c.inHand == False and c.isVisible == False and c.position == pos:
                    string = '???'
            print(string, end = ' ')    
        print('\nHAND ', end = '')
        for c in game:
            if c.player == 'B' and c.inHand == True and c.isPlayed == False:
                print(c.name(), end = ' ')
        print('\n')
