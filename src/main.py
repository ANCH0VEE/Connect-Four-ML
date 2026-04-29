import pygame
from pygame.locals import *

from board import Board
from mcts import MCTS_Node

import threading
from copy import deepcopy

pygame.init()
clock = pygame.time.Clock()
FPS = 60

pygame.init()
pygame.font.init()
FONT = pygame.font.SysFont("Arial", 24)

pygame.display.set_caption("Connect Four RL")

TILE_SIZE = 64
display_mode = (7*TILE_SIZE, (6+1)*TILE_SIZE)
display = pygame.Surface(display_mode, pygame.SRCALPHA)
screen = pygame.display.set_mode(display_mode)

# Game class: handles everything
class Game:
    def __init__(self):
        # board
        self.board = Board(self)

        # game state
        self.end_game = False
        self.winner = 0

        # moves
        self.player_move_made = False
        self.machine_started = False
        self.machine_move = None

        # mouse
        self.mouse_pos = None
        self.mouse_grid_coord = [0,0]

        # colors
        self.colors = {
            -1: (227,227,138),
            1: (223,153,138)
        }

    # eventhandler
    def eventhandler(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.MOUSEBUTTONUP:
                if self.board.get_current_player() == 1:
                    self.player_move_made = True

        self.mouse_pos = pygame.mouse.get_pos()
        # get grid coordinate of mouse cursor
        self.mouse_grid_coord[0] = self.mouse_pos[0]//TILE_SIZE
        self.mouse_grid_coord[1] = self.mouse_pos[1]//TILE_SIZE

    def thread_process(self):
        board_copy = deepcopy(self.board)
        move = MCTS_Node.MCTS_search(board_copy, 1000)
        self.machine_move = move

    # draw the 6 by 7 grid
    def draw_grid(self):
        # verticals
        for i in range(0, 8):
            x_pos = i*TILE_SIZE
            pygame.draw.line(display, (100,100,100), (x_pos, TILE_SIZE), (x_pos, display.get_height()), 2)
        # horizontals
        for i in range(0, 7):
            y_pos = i*TILE_SIZE
            pygame.draw.line(display, (100,100,100), (0, y_pos), (display.get_width(), y_pos), 2)
    
    # draw red and yellow game pieces
    def draw_pieces(self):
        for coord in self.board.red:
            pygame.draw.rect(display, self.colors[1], (coord[0]*TILE_SIZE+2, (coord[1]+1)*TILE_SIZE+2, TILE_SIZE-2, TILE_SIZE-2))
        for coord in self.board.yellow:
            pygame.draw.rect(display, self.colors[-1], (coord[0]*TILE_SIZE+2, (coord[1]+1)*TILE_SIZE+2, TILE_SIZE-2, TILE_SIZE-2))

    # highlights which column is currently selected
    def draw_current_col(self):
        if self.board.get_current_player() == 1 and self.winner == 0: # player turn
            for i in range(6):
                pygame.draw.rect(display, (70,70,70), (self.mouse_grid_coord[0]*TILE_SIZE+2, (i+1)*TILE_SIZE+2, TILE_SIZE-2, TILE_SIZE-2))

    def draw_text(self, text, pos, color):
        rendered_text = FONT.render(text, True, color)
        display.blit(rendered_text, pos)

    def write_all(self):
        if self.winner == 0:
            player = self.board.get_current_player()
            text = "turn"
            turn = "machine" if player == -1 else "player"
            color = self.colors[player]
            self.draw_text(f"{turn} {text}", (10,10), color)
        elif self.board.full_board() == True:  # tie
            self.draw_text("tie game", (10,10), (200,200,200))
        else:
            player = self.board.get_last_player()
            turn = "machine" if player == -1 else "player"
            color = self.colors[player]
            self.draw_text(f"{turn} wins", (10,10), color)

    # render, pygame display update.
    def render(self):
        display.fill((20,20,30))
        self.draw_grid()
        self.draw_current_col()
        self.draw_pieces()
        self.write_all()

        screen.blit(pygame.transform.scale(display, screen.get_size()), (0,0))
        pygame.display.update()
        clock.tick(FPS)

    def play(self):
        # TODO: thread these processes?
        if (self.board.full_board() == True):
            self.end_game = True
        
        col = None
        if self.board.get_current_player() == 1: # player
            if self.player_move_made == True:
                self.player_move_made = False
                col = self.mouse_grid_coord[0]
                if 0 <= col < 7 and self.board.find_next_in_col(self.board.board, col):
                    self.board.place_move(self.board.board, self.board.get_current_player(), col)

        elif self.board.get_current_player() == -1: # machine
            # start threading only once
            if self.machine_started == False:
                self.machine_started = True
                self.machine_move = None

                threading.Thread(target=self.thread_process,daemon=True).start()

            # make move
            if self.machine_move != None:
                col = self.machine_move[0]

                self.board.place_move(self.board.board, -1, col)

                self.machine_move = None
                self.machine_started = False

        # check if any player has won, based on last move played
        if (self.board.check_win_state(self.board.board, self.board.last_played) == True):
            self.end_game = True
            self.winner = self.board.get_last_player()

    # main game loop
    def main(self):
        while True:
            self.eventhandler()

            if self.end_game != True:
                self.play()
            
            self.render()

# make game
game = Game()
if __name__ == "__main__":
    game.main()