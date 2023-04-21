from math import *
import random
from tools_temp import *
from ismcts_state import *
## code adapted from https://github.com/melvinzhang/ismcts/blob/master/ISMCTS.py

#TODO: UCBSELECTCHILD: change exploration & try different formulae

joker = Card(-1,-1,'None', False, False, -1, False)
class Node:
    """ A node in the game tree. Note wins is always from the viewpoint of playerJustMoved.
    """

    def __init__(self, move=None, parent=None, playerJustMoved=None):
        self.move = move  # the move that got us to this node - "None" for the root node. moves are cards. we can infer player by looking at self.playerJustMoved.
        self.parentNode = parent  # "None" for the root node
        self.childNodes =[]                                                 
        self.wins = 0       # wins will be "score"
        self.visits = 0     # times going through that node
        self.avails = 1     # times going through a sibling of our node
        self.playerJustMoved = (
            playerJustMoved
        )  # the only part of the state that the Node needs later

    def GetUntriedMoves(self, legalMoves): #legalmoves are found by GetMoves
        """ Return the elements of legalMoves for which this node does not have children.
        """

        # Find all moves for which this node *does* have children
        triedMoves = [child.move for child in self.childNodes]

        # Return all moves that are legal but have not been tried yet
        return [move for move in legalMoves if move not in triedMoves]

    def UCBSelectChild(self, legalMoves, exploration=0.7): #TODO: change exploration eventually
        """ Use the UCB1 formula to select a child node, filtered by the given list of legal moves.
            exploration is a constant balancing between exploitation and exploration, with default value 0.7 (approximately sqrt(2) / 2)
        """

        # Filter the list of children by the list of legal moves
        legalChildren = [child for child in self.childNodes if child.move in legalMoves]

        # Get the child with the highest UCB score #TODO: try other algos.
        s = max(
            legalChildren,
            key=lambda c: float(c.wins) / float(c.visits)
            + exploration * sqrt(log(c.avails) / float(c.visits)),
        )

        # Update availability counts -- it is easier to do this now than during backpropagation
        for child in legalChildren:
            child.avails += 1

        # Return the child selected above
        return s

    def AddChild(self, m, p):
        """ Add a new child node for the move m. p is the player that did the move.
            Return the added child node. note that m is a Card.
        """
        n = Node(move=m, parent=self, playerJustMoved=p)
        self.childNodes.append(n)
        return n

    def Update(self, terminalState):
        """ Update this node - increment the visit count by one, and increase the win count by the result of terminalState for self.playerJustMoved.
        """
        self.visits += 1
        if self.playerJustMoved is not None:
            self.wins += terminalState.GetResult(self.playerJustMoved)

    def __repr__(self):
        return "[M:%s P/g//W/V/A: %4i/%4i/%4i]" % (
            self.move.name(),
            self.wins//self.visits, #modification to fit the model better
            self.visits,
            self.avails,
        )

    def TreeToString(self, indent):
        """ Represent the tree as a string, for debugging purposes.
        """
        s = self.IndentString(indent) + str(self)
        for c in self.childNodes:
            s += c.TreeToString(indent + 1)
        return s

    def IndentString(self, indent):
        s = "\n"
        for i in range(1, indent + 1):
            s += "| "
        return s

    def ChildrenToString(self):
        s = ""
        for c in self.childNodes:
            s += str(c) + "\n"
        return s
    

def ISMCTS(rootstate, itermax=100, verbose=False, exp=0.7):
    """ Conduct an ISMCTS search for itermax iterations starting from rootstate. rootstate is an instance of state
        Return the best move from the rootstate.
    """

    rootnode = Node()

    for i in range(itermax):
        node = rootnode

        # Determinize
        state = rootstate.CloneAndRandomize()

        # Select
        #print([obs.name() for obs in state.GetMoves()])
        #print([obs.name() for obs in node.GetUntriedMoves(state.GetMoves())])
        #print("")
        while (
            state.GetMoves() != [] and node.GetUntriedMoves(state.GetMoves()) == []
            
        ):  # node is fully expanded and non-terminal
        
            node = node.UCBSelectChild(state.GetMoves(), exploration=exp)
            state.DoMove(node.move)

        # Expand
        untriedMoves = node.GetUntriedMoves(state.GetMoves())
        if untriedMoves != []:  # if we can expand (i.e. state/node is non-terminal)
            m = random.choice(untriedMoves)
            player = state.player
            state.DoMove(m)
            node = node.AddChild(m, player)  # add child and descend tree

        #Simulate
        while state.GetMoves() != []:  # while state is non-terminal
            #print(len(state.GetMoves()))
            state.DoMove(random.choice(state.GetMoves()))

        # Backpropagate
        while (
            node != None
        ):  # backpropagate from the expanded node and work back to the root node
            node.Update(state)
            node = node.parentNode

    # Output some information about the tree - can be omitted
    if verbose:
       print(rootnode.TreeToString(0))
    #else:
        #print(rootnode.ChildrenToString())

    return max(
        rootnode.childNodes, key=lambda c: c.visits
    ).move  # return the move that was most visited


def PlayGame(n, agents):
    """ Play a sample game between two ISMCTS players.
    """
    state = KnockoutWhistState(n)

    while state.GetMoves() != []:
        print(str(state))
        # Use different numbers of iterations (simulations, tree nodes) for different players
        m = agents[state.playerToMove](state)
        print("Best Move: " + str(m) + "\n")
        state.DoMove(m)

    someoneWon = False
    for p in range(1, state.numberOfPlayers + 1):
        if state.GetResult(p) > 0:
            print("Player " + str(p) + " wins!")
            someoneWon = True
    if not someoneWon:
        print("Nobody wins!")