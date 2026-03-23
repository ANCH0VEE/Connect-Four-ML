#import numpy as np
import torch
import torch.nn

import random

# connect four board: 7 columns, 6 rows. Each COLUMN is a 1d array. In code, the board is sideways, with right as "top" and left as "bottom".
# player IDs: 0: empty space; 1: player 1 space; -1: player 2 space.
# turns: player = -player

class Board:
    # wins : TODO: replace with more efficient search algorithm based around last move made by certain player.
    #        just iterate and directly use the index instead
    """vertical_win = [
        '''(0,0),'''
        (1,0),
        (2,0),
        (3,0)
    ]
    horizontal_win = [
        '''(0,0),'''(0,1),(0,2),(0,3)
    ]
    TL_BR_win = [
        '''(0,0),'''
            (1,1),
                (2,2),
                    (3,3)
    ]
    BR_TL_win = [
                    (-3,3),
                (-2,2),
            (-1,1),
        '''(0,0)''' 
    ]"""
    def __init__(self):
        #self.gameboard = np.zeros((7,6), dtype=np.int8) # coordinates for np array: (row number, row index).
        self.gameboard = torch.zeros((7, 6), dtype=torch.int8)

        # ----- testing: delete this after
        height = 6
        for i in range (6):
            for j in range (height):
                self.gameboard[i][-j-1] = 1
            height -=1

        '''for i in range (4):
            self.gameboard[0][i] = -1'''
        # -----

        self.player_turn = 1 # 1 and -1.
        self.last_played = [None, None]

    # TODO: might not need all of these, we will see
    def get_current_player(self): # 1 and -1
        return self.player_turn
    def switch_current_player(self):
        self.player_turn = -self.player_turn
    def get_last_player(self):
        return -self.player_turn

    # returns coordinate of next spot in a column (last 0)
    def find_next_in_col(self, col):
        zero_indices = torch.nonzero(self.gameboard[col] == 0).squeeze(1) # a tuple
        if (zero_indices.numel() > 0):
            # The "highest" index is the one closest to the floor (Right side)
            next_spot = zero_indices[-1].item()
            return [col, next_spot]
        return None
    
    # return grid coordinates. any completely filled column will not have a possible move in that column.
    # TODO: or would this be all available columns? all cols available unless filled to top.
    def get_all_possible_moves(self):
        available_moves = []
        for col in range(7):
            # get highest index that contains a zero
            move = self.find_next_in_col(col)
            available_moves.append(move) if move != None else None
        return available_moves

    # TODO: make sure to check, before calling this method, whether col is valid (still has open space).
    #       or instead, do we check inside the method itself?
    def place_move(self, player_turn, col):
        coords = self.find_next_in_col(col)
        self.gameboard[coords[0]][coords[1]] = player_turn
        self.last_played = coords
        self.switch_current_player()
        self.print_info()

    def place_random_move(self, player_turn):
        rand_col = random.choice(self.get_all_possible_moves())[0] # automatically filters out invalid cols
        self.place_move(player_turn, rand_col)

    # TODO: for efficiency, check around last placed piece: "search algorithm"
    def check_win_state(self, game_state, last_coord):
        # from previous move (coordinate), get all pieces of same player that are touching previous move horizontally, vertically, or diagonally.
        last_id = game_state[last_coord[0]][last_coord[1]]
        for i in range (4):
            pass

    # TODO: game board full as one of first checks in game loop
    def full_board(self):
        pass


    def print_info(self):
        print('v top left side')
        print(self.gameboard)
        print('^ top right side')

        # matrix transpose for proper view.
        print("\n transpose: proper game board display")
        print(self.gameboard.T)

        print("all possible moves left: ", b.get_all_possible_moves())
        print(f"player {self.get_last_player()} just played {self.last_played}")
        print("---------------------------")

    def main(self):
        pass

b = Board()

b.print_info()
for i in range(2):
    b.place_move(b.player_turn, 2)

for i in range(10):
    b.place_random_move(b.player_turn)