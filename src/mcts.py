import math, random
from copy import deepcopy

# TODO: Add heuristics. mcts works, but game still misses easy wins, or fails to block opponent wins. 
# TODO: introduce/train neural net at the expansion phase to choose a non-random move.

# MCTS node class
class MCTS_Node:
    # perform all four phases of MCTS to (hopefully) find the best move
    def MCTS_search(game, iterations):
        #                                                  get last player (1, person), because we want current move decision.
        root = MCTS_Node(game, game.board, None, None, game.get_last_player())

        # perform all iteration of MCTS, grow the tree.
        for i in range (iterations):
            node = root
            # selection
            while node.is_terminal() == False and node.is_fully_expanded() == True:
                node = node.best_child()
            # expansion
            if node.is_terminal() == False and node.is_fully_expanded() == False:
                node = node.expand()
            # simulation
            winner = node.simulation()
            # backpropogation
            node.backpropogate(winner)

        # return the best action (most visits)
        best = None
        for child in root.children:
            if best == None or child.visits > best.visits:
                best = child
        return best.action # a tuple

    def __init__(self, game, state, parent, action, player):
        self.game = game # reference to game
        self.state = state
        self.parent = parent # parent node
        self.action = action # (x,y)
        self.player = player # which player turn

        self.children = [] # children of this node
        self.visits = 0
        self.wins = 0.0
        self.untried_actions = self.game.get_all_possible_moves(self.state) # a list of tuples (x,y)

    # am I a terminal node? (is there a win or tie in my game state?)
    def is_terminal(self):
        if self.action == None:
            return False # root node
        return (self.game.check_win_state(self.state, self.action) or len(self.game.get_all_possible_moves(self.state)) == 0)

    # does this node have a child node of a game state that it hasn't been created yet in the tree?
    def is_fully_expanded(self):
        return len(self.untried_actions) == 0
    
    # based on UCB1, choose the next child with the highest UCB1 value. used in the selection phase.
    def best_child(self, c=1.4):
        # this is here to avoid a divide by zero problem and to enforce guaranteed exploration?
        for child in self.children:
            if child.visits == 0:
                return child

        def ucb(child):
            exploit = child.wins/child.visits
            explore = c*math.sqrt(math.log(self.visits)/child.visits)
            return exploit+explore
        
        best = None
        for child in self.children:
            if best == None or ucb(child) > ucb(best):
                best = child
        return best

    # expansion phase: we are at a leaf node in the current tree: choose and add a child for the leaf.
    def expand(self): # expansion phase
        # pop to remove from untried actions.
        action = random.choice(self.untried_actions) # random
        self.untried_actions.remove(action) 

        new_state = deepcopy(self.state) # create a brand new state to put into a new MCTS_Node object: do not want to change the one for current node.
        next_player = -self.player
        new_state[action[0]][action[1]] = next_player

        child = MCTS_Node(self.game, new_state, self, action, next_player)
        self.children.append(child)
        return child
    
    # simulation phase (rollout): make tree copy and simulate a game with random moves. then return player if win, None if tie/loss.
    def simulation(self):
        state = deepcopy(self.state)
        player = self.player
        last_move = None

        while True: # until a return statement (draw or winner player -1/1)
            actions = self.game.get_all_possible_moves(state)
            if len(actions) == 0: # draw
                return None

            move = random.choice(actions)
            state[move[0]][move[1]] = player
            last_move = move

            winner = self.game.check_win_state(state, last_move)
            if winner == True:
                return player

            player = -player

    # backpropogation phase: update node data from this iteration's new tree node back up to the root node.
    def backpropogate(self, winner):
        self.visits +=1

        if winner == self.player:
            self.wins += 1.0
        
        # will a stricter reward system be better?
        '''elif winner == None:
            self.wins += 0.0
            #self.wins += 0.5'''

        # call method on parent until root node (has no parent).
        if self.parent != None:
            self.parent.backpropogate(winner)