import math
import random
from copy import deepcopy

BOARD_SIZE = 3

# after a move, check if any 3 in a row (8 win combos)
def check_winner_state(state):
    for i in range(BOARD_SIZE):
        if state[i][0] == state[i][1] == state[i][2] != 0:
            return state[i][0]
        if state[0][i] == state[1][i] == state[2][i] != 0:
            return state[0][i]
    if state[0][0] == state[1][1] == state[2][2] != 0:
        return state[0][0]
    if state[0][2] == state[1][1] == state[2][0] != 0:
        return state[0][2]
    return None

# return list of empty spaces
def available_actions(state):
    return [(i, j) for i in range(BOARD_SIZE) for j in range(BOARD_SIZE) if state[i][j] == 0]

# count x's and o's, determine whose move it is next by their counts.
def get_current_player(state):
    x_count = sum(row.count(1) for row in state)
    o_count = sum(row.count(2) for row in state)
    return 1 if x_count == o_count else 2

# one node in the tree.
class MCTSNode:
    def __init__(self, state, parent=None, action=None, player=None):
        self.state = state
        self.parent = parent
        self.action = action        
        self.player = player         
        self.children = []
        self.visits = 0
        self.wins = 0.0
        self.untried_actions = available_actions(state)

    def is_terminal(self):
        return check_winner_state(self.state) is not None or not available_actions(self.state)
    
    # full board
    def is_fully_expanded(self):
        return len(self.untried_actions) == 0
    def expand(self):
        action = self.untried_actions.pop()
        new_state = deepcopy(self.state)
        player_to_move = get_current_player(self.state)
        new_state[action[0]][action[1]] = player_to_move

        child = MCTSNode(new_state, parent=self, action=action, player=player_to_move)
        self.children.append(child)
        return child
    def best_child(self, c=1.4):
        for child in self.children:
            if child.visits == 0:
                return child

        def ucb(child):
            exploit = child.wins / child.visits
            explore = c * math.sqrt(math.log(self.visits) / child.visits)
            return exploit + explore

        return max(self.children, key=ucb)
    
    def rollout(self):
        state = deepcopy(self.state)
        player = get_current_player(state)

        while True:
            winner = check_winner_state(state)
            if winner is not None:
                return winner
            actions = available_actions(state)
            if not actions:
                return None
            move = random.choice(actions)
            state[move[0]][move[1]] = player
            player = 1 if player == 2 else 2

    def backpropagate(self, winner):
        self.visits += 1

        if self.player is not None:
            if winner is None:
                self.wins += 0.5
            elif winner == self.player:
                self.wins += 1.0

        if self.parent:
            self.parent.backpropagate(winner)




def mcts_search(root_state, iterations=500):
    root = MCTSNode(root_state, player=None)

    for _ in range(iterations):
        node = root

        while not node.is_terminal() and node.is_fully_expanded():
            node = node.best_child()

        if not node.is_terminal() and not node.is_fully_expanded():
            node = node.expand()

        winner = node.rollout()
        node.backpropagate(winner)

    best = max(root.children, key=lambda c: c.visits)
    return best.action

# main
def play_game():
    board = [[0]*3 for _ in range(3)]
    current_player = 1

    print("MCTS Tic-Tac-Toe Demo")
    print("0 = empty, 1 = X, 2 = O\n")

    for turn in range(9):
        for row in board: print(row)
        print()

        if current_player == 1:
            move = mcts_search(board, iterations=300)
            print(f"MCTS plays: {move}")
        else:
            empty = available_actions(board)
            move = random.choice(empty)
            print(f"Random plays: {move}")

        board[move[0]][move[1]] = current_player

        winner = check_winner_state(board)
        if winner:
            for row in board: print(row)
            print(f"Player {winner} wins!")
            return

        current_player = 1 if current_player == 2 else 2

    print("Draw!")

if __name__ == "__main__":
    play_game()