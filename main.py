#import numpy as np
import torch
import torch.nn

import random

# connect four board: 7 columns, 6 rows. Each COLUMN is a 1d array. In code, the board is sideways, with right as "top" and left as "bottom".
# player IDs: 0: empty space; 1: player 1 space; -1: player 2 space.
# turns: player = -player

# IMPORTANT: pretend that connect four is 7x6, and we insert pieces from the left and they fall to the right.
class Board:
    def __init__(self):
        #self.gameboard = np.zeros((7,6), dtype=np.int8) # coordinates for np array: (row number, row index).
        self.gameboard = torch.zeros((7, 6), dtype=torch.int8)
        self.movesPlayed = 0; 

        self.player_turn = 1 # 1 and -1. to train NN, can do: board *= -1 (player turn doesn't matter when training nn).
        self.last_played = [None, None]

        # dummy board ---
        '''height = 6
        for i in range (6):
            for j in range (height):
                self.gameboard[i][-j-1] = 1
            height -=1'''
        
        # -----
        '''for i in range (4):
            for i in range (4):
                self.place_move(self.get_current_player(), i)'''
        
        # list of columns in which moves are placed, in order by index. alternates between players 1 and -1.
        # tests
        horizontal_test_move_sequence= [0,6,1,6,2,6,3]
        vertical_test_move_sequence= [0,6,0,5,0,4,0]
        diagonal_test_move_sequence_TLBR = [0,1,2,3,4,0,1,2,2,3,3,6,3]
        diagonal_test_move_sequence_BLTR = [0,1,2,3,4,0,1,2,4,3,2,3,3]
        #self.test_sequence_of_moves(diagonal_test_move_sequence_TLBR)
            
        # -----------------

    def test_sequence_of_moves(self, list):
        for col in list:
            self.place_move(self.get_current_player(), col)

    # might not need all of these, we will see
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
        self.movesPlayed+=1
        coords = self.find_next_in_col(col)
        self.gameboard[coords[0]][coords[1]] = player_turn
        self.last_played = coords
        self.switch_current_player()
        #self.print_info()

    def place_random_move(self, player_turn):
        rand_col = random.choice(self.get_all_possible_moves())[0] # automatically filters out invalid cols
        self.place_move(player_turn, rand_col)

    def check_win_state(self, game_state, coords):
        if coords[0] == None: return False # this is for empty board check, when no moves have been made yet
        # from previous move (coordinate), get all pieces of same player that are touching previous move horizontally, vertically, or diagonally.
        color = self.get_last_player() # returns 1 if red, -1 if yellow
        # (x,y) is the last played move by color
        x = coords[0] # row
        y = coords[1] # col

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
        return self.movesPlayed == 42

    def print_info(self):
        print('v top left side')
        print(self.gameboard)
        print('^ top right side')

        # matrix transpose for proper view.
        print("\n transpose: proper game board display")
        print(self.gameboard.T)

        print("all possible moves left: ", self.get_all_possible_moves())
        print(f"player {self.get_last_player()} just played {self.last_played}")
        print("---------------------------")

    # main game loop
    def main(self):
        end_game = False
        winner = None
        while (end_game == False):
            if (self.full_board() == True):
                end_game = True
                break

            print(self.gameboard.T)
            while True:
                try: # keep prompting user until input is 0-6 and that the column has space available (not full col)
                    col = int(input(f"player {self.get_current_player()} turn: insert into column with space (0-6): "))
                    if 0 <= col <= 6 and self.find_next_in_col(col) != None:
                        break
                except ValueError:
                    pass

            self.place_move(self.get_current_player(), col)

            if (self.check_win_state(self.gameboard, self.last_played) == True):
                end_game = True
                winner = self.get_last_player()

            print("four in a row:", self.check_win_state(self.gameboard, self.last_played))
            print("--------------------")
            #self.print_info()

        if (winner == None):
            print("IT'S A TIE!")
            print(self.gameboard.T)
        else:
            print("FOUR IN A ROW!")
            print(self.gameboard.T)
            print(f"WINNER:", winner)

b = Board()
if __name__ == "__main__":
    b.main()