# 26.03
# objective: generate a certain number of games that are sort of even aka initial player score is 81+-15. Moreover, they have at least three trumps each (clubs)
# idea: identify these games with a starter id (a sequence of 10 numbers of 1-32). At the start of the game, we pick a game among all the possible identifiers. Then for each rollout, we generate a game that correspond to the same id.
#if we say the MCTS will do ~10k simulation for each rollout then we want maybe... ~2k game for the same identifier.
# the number of id is unknown to me yet, but probably <100 as no two player will play more than 100 games together.
# the games are a series of 32 numbers. first 5 are A vis, 5 B vis, 5 A hidden, 5 B hidden, 6 A hand, 6B hand.

import random
import os
import two_belote

K = 10000
def main():
    for t in range(100):
        print('id: '+str(t))
        gen()

def gen():
    # generate one game id + the K associated games.
    name, cards, nL = gen_id()
    f = open(name, 'w') # create the file and open it
    visA, visB = cards[:5], cards[5:]
    rem_points = 162 - points(visA + visB)
    A = points(visA)
    B = points(visB)
    # we have rem_points to distribute to both player. Ideally, if pA and pB are the remaining split, we want:
    # 61 < A+pA < 101           ## NOTE: actually its 56, 96 because there is only 152 points for cards & 10 for last round.
    # 61 < B+pB < 101
    # with pA + pB = rem_points
    # eq. pA = rem_points -pB
    # eq. 61 < A + rem_points - pB < 101 and 61 < B + pB < 101
    # eq 61-B < pB < 101 -B

    for k in range(K):
        flag = False
        while flag == False:
            pB = 0
            av = nL.copy()
            cards_B = []
            for i in range(11):    
                c = random.choice(av)
                av.remove(c)
                cards_B.append(conversion_int_card(c))
            pB = points(cards_B)
            if 56-B < pB and pB < 96-B and 56 < A + rem_points - pB and A + rem_points-pB < 96:
                flag = True

        cards_A = [conversion_int_card(c) for c in av.copy()]
        game = cards + cards_A+cards_B
        line = ''
        for obs in game:
            line += str(obs[0]) + str(obs[1]) +' '
        line += '\n'
        f.write(line)
    f.close()

def points(L, trump = 0):
    """ count the # of points of a given sequence"""
    r = 0
    val_trump = [20,14,11, 10, 4, 3, 0, 0]
    val = [11, 10, 4, 3, 2, 0, 0, 0]
    for c in L:
        r += (trump == two_belote.col(c))*val_trump[two_belote.index(c)] + (trump != two_belote.col(c))*val[two_belote.index(c)]
    return r
        
def gen_id():
    # generate a game id + card values
    av = [i for i in range(32)]
    nL= []
    cardList = []
    while len(nL) != 10:
        c = random.choice(av)
        av.remove(c)
        nL.append(c)
        cardList.append(conversion_int_card(c))
    name = ''
    for n in nL:
        name+=str(n)+'.'

    return name+'txt', cardList, av

def conversion_int_card(id):
    #return the card format of id.
    return (id//8, id%8)

main()