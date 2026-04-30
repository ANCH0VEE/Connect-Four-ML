import torch
import torch.nn
import pygame
from copy import deepcopy

from mcts import MCTS_Node

# connect four board: 7 columns, 6 rows. Each COLUMN is a 1d array. In code, the board is sideways, with right as "top" and left as "bottom".
# player IDs: 0: empty space; 1: player 1 space; -1: player 2 space.
# turns: player = -player

# IMPORTANT: pretend that connect four is 7x6, and we insert pieces from the left and they fall to the right.
class Board:
    def __init__(self, game):
        self.game = game
        self.board = torch.zeros((7, 6), dtype=torch.int8)
        self.moves_played = 0; 

        self.player_turn = 1 # 1 and -1. to train NN, can do: board *= -1 (player turn doesn't matter when training nn).
        self.last_played = None

        self.red = []
        self.yellow = []

    # might not need all of these, we will see
    def get_current_player(self): # 1 and -1
        return self.player_turn
    def switch_current_player(self):
        self.player_turn = -self.player_turn
    def get_last_player(self):
        return -self.player_turn

    # returns coordinate of next spot in a column (last 0)
    def find_next_in_col(self, game_state, col):
        zero_indices = torch.nonzero(game_state[col] == 0).squeeze(1) # a tuple
        if (zero_indices.numel() > 0):
            # The "highest" index is the one closest to the floor (Right side)
            next_spot = zero_indices[-1].item()
            return [col, next_spot]
        return None
    
    # returns columns (indices) with open moves
    '''def find_open_cols(self, game_state):
        open_cols = []
        for i in range (7):
            zero_indices = torch.nonzero(game_state[i] == 0).squeeze(1) # a tuple
            if (zero_indices.numel() > 0):
                open_cols.append(i)
        return open_cols'''
        
    # return grid coordinates. any completely filled column will not have a possible move in that column.
    def get_all_possible_moves(self, game_state):
        available_moves = []
        for col in range(7):
            # get highest index that contains a zero
            move = self.find_next_in_col(game_state, col)
            available_moves.append(move) if move != None else None
        return available_moves

    # current player places piece in column
    def place_move(self, game_state, player_turn, col):
        self.moves_played+=1
        coords = self.find_next_in_col(game_state, col)

        # add to lists
        if self.get_current_player() == -1: self.yellow.append(coords)
        else: self.red.append(coords)

        game_state[coords[0]][coords[1]] = player_turn
        self.last_played = coords
        self.switch_current_player()

    # place a random move
    '''def place_random_move(self, game_state, player_turn):
        rand_col = random.choice(self.get_all_possible_moves(game_state))[0] # automatically filters out invalid cols
        self.place_move(player_turn, rand_col)'''

    # returns if a player has won, based on last move played.
    # from previous move (coordinate), get all pieces of same player that are touching previous move horizontally, vertically, or diagonally.
    def check_win_state(self, game_state, coords):
        if coords == None:
            return False # this is for empty board check, when no moves have been made yet

        # (x,y) is the last played move by color
        x = coords[0] # row
        y = coords[1] # col
        color = game_state[x][y]

        # check horizontal
        consecutive_color = 1
        for direction in [1,-1]:
            i = 1 # magnitude of offset from last played chip ("middle")
            #                           v  meaning 6th item 
            while (0 <= y+direction*i <= 5 and game_state[x][y+direction*i] == color):
                consecutive_color +=1
                i+=1
        if consecutive_color >= 4:
            return True
        
        # check vertical
        consecutive_color = 1
        for direction in [-1,1]:
            i = 1
            while (0 <= x+direction*i <= 6 and game_state[x+direction*i][y] == color):
                consecutive_color +=1
                i+=1
        if consecutive_color >= 4:
            return True
        
        # check diagonal (1)
        num_in_a_row = 1
        for direction in [-1,1]:
            i = 1
            while (0 <= y+direction*i <= 5 and 0 <= x+direction*i <= 6
                   and game_state[x+direction*i][y+direction*i] == color):
                num_in_a_row +=1
                i+=1
        if num_in_a_row >= 4:
            return True
        
        # check diagonal (2)
        num_in_a_row = 1
        for direction in [-1,1]:
            i = 1
            while (0 <= y-direction*i <= 5 and 0 <= x+direction*i <= 6
                   and game_state[x+direction*i][y-direction*i] == color):
                num_in_a_row +=1
                i+=1
        if num_in_a_row >= 4:
            return True

        # no 4 in a row
        return False

    def full_board(self):
        return self.moves_played == 42
    
    # heuristics
    def easy_win_heuristic(self):
        check_moves = self.get_all_possible_moves(self.board)
        for i in range(7):
            dummy_board = deepcopy(self.board)
            self.place_move(dummy_board, self.get_current_player(), check_moves[i][1])
            if (self.check_win_state(dummy_board, check_moves[i]) == True):
                self.place_move(self.board, self.get_current_player(), i)
                print("easy win found")
                return True
        return False