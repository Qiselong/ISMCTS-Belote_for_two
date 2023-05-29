#date 25/05/23
#compile results of files of the form "logs*.txt" and produce images out of it.
import matplotlib.pyplot as plt

def main():
    pat = "logs*.txt"
    file_list = find(pat, '../')
    games = gather(file_list)
    print(f'Grand total of {len(games)} games analyzed.')
    print(len([1 for g in games if g[1]>81]))
    box_plots(games)
    hist(games)

import os, fnmatch
def find(pattern, path): #source: https://stackoverflow.com/questions/1724693/find-a-file-in-python
    result = []
    for root, dirs, files in os.walk(path):
        for name in files:
            if fnmatch.fnmatch(name, pattern):
                result.append(os.path.join(root, name))
    return result

def gather(file_list):
    ''' return the game list under [[run, pts]] format.'''
    games = []
    for fi in file_list:
        f = open(fi, 'r')
        for l in f:
            game = l[:len(l)-1]
            run, pt = game.split(';')
            pt = int(pt)
            games.append([run, pt])
    return games

def box_plots(games, name='../boxplot'):
    '''given the list of games print a boxplot figure with 3 boxes (A first, B first, all)'''

    A_games = [g[1] for g in games if g[0][0] == 'A']
    B_games = [g[1] for g in games if g[0][0] == 'B']
    all_games = [g[1] for g in games]
    fig1, ax1 = plt.subplots()
    ax1.boxplot([A_games, B_games, all_games])
    ax1.set_title("Average score for the ISMCTS player (A) given the first move")
    plt.xticks([1, 2, 3], ['A', 'B', 'Total'])
    
    left, right = plt.xlim()
    plt.hlines(81, xmin=left, xmax=right, color='r', linestyles='--')
    plt.savefig(name)
    #plt.show()

def hist(games, name='../history'):
    G = [g[0][1:] for g in games] #remove 1st, non useful element
    N = len(G)
    nwin = [0 for i in range(16)]
    for i in range(16):
        k = 0
        for g in G:
            k += (g[i] == 'A')
        nwin[i] = k

    pwin = [100*k/N for k in nwin]
    
    # then we have in nwin(t) the number of games where round t was won by player A.
    fig2, ax1 = plt.subplots()
    
    ax1.set_title("Win percentage of ISMCTS player by round")
    ax1.bar([i for i in range(16)],pwin)
    plt.xticks([i for i in range(16)],[i+1 for i in range(16)])
    left, right = plt.xlim()
    plt.hlines(50, xmin=left, xmax=right, color='r', linestyles='--')
    #plt.show()
    plt.savefig(name)
main()