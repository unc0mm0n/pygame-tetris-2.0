import pygame
from pygame.locals import *
from utils import *
from tetris import *

PIECE_SIZE  =4
WORLD_SIZE = Vector((36, 24))
BLOCK_SIZE = 20

BOARD_SIZE = Vector((10, 22))


class TetrisGame(object):

    '''
        Handles the UI of a basic tetris game.
    '''

    def __init__(self):
        pygame.display.set_caption('Testris 2.0!!')
        self.window = pygame.display.set_mode(tuple(WORLD_SIZE * BLOCK_SIZE))
        self.screen = pygame.display.get_surface()
        self.clock = pygame.time.Clock()
        self.world = Rect((0, 0), tuple(WORLD_SIZE))

        self.board = Rect(tuple(WORLD_SIZE / 2 - BOARD_SIZE / 2), BOARD_SIZE)
        self.tetris = Tetris(PIECE_SIZE, *WORLD_SIZE)

        self.start()

    def start(self):
        self.tetris.reset()
        self.playing = True

    def update(self, dt):
        '''Update the tetris object by dt time, passing any movement orders.'''
        self.playing = self.tetris.update(dt)

        for cell in self.tetris.board:
            print(self.get_block(self.get_coor_from_board(cell)), end=" ")
        print('\n\n\n')

    def get_coor_from_board(self, loc):
        '''Returns the coordinate of an (x, y) coordinate inside the board.'''
        return self.board.topleft + loc

    def get_block(self, loc):
        width = RIGHT * BLOCK_SIZE
        height = DOWN * BLOCK_SIZE
        loc = loc * BLOCK_SIZE
        return Rect(tuple(loc), tuple(width + height))

if __name__ == '__main__':
    pygame.init()
    t = TetrisGame()
    while t.playing:
        t.update(1000)

