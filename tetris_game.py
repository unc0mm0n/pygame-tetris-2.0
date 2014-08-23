import pygame
from pygame.locals import *
from utils import *
from tetris import *

PIECE_SIZE = 4
WORLD_SIZE = Vector((36, 24))
BLOCK_SIZE = 20

BOARD_SIZE = Vector((10, 22))
TEXT_LOCATION = Vector((-5, 5))

BG_COLOR = (0, 0, 0)
BORDER_COLOR = (160, 160, 160)
TEXT_COLOR = (255, 255, 255)

MOVE_KEYS = {
    K_LEFT: LEFT,
    K_RIGHT: RIGHT
}

ROTATE_KEYS = {
    K_UP: -1,
    K_DOWN: 1
}


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
        self.font = pygame.font.Font(pygame.font.get_default_font(), 22)

        self.board = Rect(tuple(WORLD_SIZE / 2 - BOARD_SIZE / 2), BOARD_SIZE)
        self.text_position = self.board.topleft + TEXT_LOCATION
        self.tetris = Tetris(PIECE_SIZE, *BOARD_SIZE)

        self.start()

    def start(self):
        '''Start a game of tetris, reseting the tetrist object.'''
        self.tetris.reset()
        self.next_move = None
        self.next_rotate = None
        self.playing = True
        self.play()

    def update(self, dt):
        '''Update the tetris object by dt time, passing any movement orders.'''
        self.playing = self.tetris.update(dt, self.next_move, self.next_rotate)
        self.next_rotate = None
        self.next_move = None

    def draw(self):
        '''Draw self into the screen.'''
        self.screen.fill(BG_COLOR)

        self.draw_borders()

        for cell, color in self.tetris.get_board().items():
            rect = self.get_block(self.get_coor_from_board(cell), 1)
            pygame.draw.rect(self.screen, color, rect)

        self.draw_text('Lines:', self.get_block(self.text_position))

        score = self.tetris.lines
        score_position = Vector(self.text_position) + DOWN
        self.draw_text(str(score), self.get_block(score_position))

        pygame.display.flip()

    def play(self):
        '''Plays the game, handling user input.'''
        while True:
            dt = self.clock.tick(60)

            for e in pygame.event.get():
                if e.type == QUIT:
                    return
                elif e.type == KEYDOWN:
                    self.input(e.key)

            if self.playing:
                self.update(dt)
            self.draw()

    def input(self, e):
        '''Handles keyboard input.'''
        if e in MOVE_KEYS:
            self.next_move = MOVE_KEYS[e]
        elif e in ROTATE_KEYS:
            self.next_rotate = ROTATE_KEYS[e]
        elif e == K_SPACE:
            if self.playing:
                self.tetris.drop_piece()
            else:
                self.start()

    def draw_text(self, text, block, color=TEXT_COLOR):
        '''Draws text on screen at block.'''
        self.screen.blit(self.font.render(text, 1, color), block)

    def draw_borders(self):
        '''Draw the border around the board.'''
        for y in range(self.board.height):
            rect = self.get_block(self.get_coor_from_board(Vector((-1, y))))
            pygame.draw.rect(self.screen, BORDER_COLOR, rect)

            right_border = Vector((self.tetris.width + 1, y))
            rect = self.get_block(self.get_coor_from_board(right_border))
            pygame.draw.rect(self.screen, BORDER_COLOR, rect)

        for x in range(-1, self.board.width + 1):
            right_border = Vector((x, self.tetris.height + 1))
            rect = self.get_block(self.get_coor_from_board(right_border))
            pygame.draw.rect(self.screen, BORDER_COLOR, rect)

    def get_coor_from_board(self, loc):
        '''Returns the coordinate of an (x, y) coordinate inside the board.'''
        return self.board.topleft + loc

    def get_block(self, loc, padding=0):
        padding = Vector((padding, padding))
        width = RIGHT * BLOCK_SIZE
        height = DOWN * BLOCK_SIZE
        loc = loc * BLOCK_SIZE + padding

        try:
            return Rect(tuple(loc), tuple(width + height) - padding*2)
        except e:
            print('Error when drawing: ', loc, e)
            return Rect(0, 0, 0, 0)

if __name__ == '__main__':
    pygame.init()
    t = TetrisGame()
    pygame.quit()
