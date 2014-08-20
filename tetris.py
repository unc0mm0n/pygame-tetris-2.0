from piece import *
from time import sleep

BG_COLOR = (0, 0, 0)

PIECE_COLORS = {
    'RED': (255, 0, 0),
    'GREEN': (0, 255, 0),
    'BLUE': (0, 0, 255),
    'YELLOW': (0, 255, 255)
}

WIDTH = 10
HEIGHT = 22


class Tetris(object):

    '''
    Tetris object that handles a tetris game with pieces of given size.
    Use reset() to start a new game.
    '''

    def __init__(self, size=4):
        '''Init with a optional size parameter for the size of each piece.'''
        self.size = size
        self.width = WIDTH
        self.height = HEIGHT
        self.reset()

    def reset(self):
        '''Restart the game.'''
        self.board = []
        self.playing = True
        self.piece = None
        self.update()

    def piece_can_down(self, piece):
        '''  Returh True if the given piece can go down without leaving the
            Board or coliding with another piece.'''
        new_piece = piece.copy()
        new_piece.move(DOWN)
        for cell in new_piece:
            print(cell)
            if cell[1] > self.height:
                return False
            if len([coor for coor in self.board if cell in coor]) > 0:
                return False
        return True

    def update(self):
        '''Move the game one step forward.'''
        if not self.piece:
            color = choice(tuple(PIECE_COLORS.values()))
            pos = Vector((self.width // 2, 0))
            self.piece = Piece.Random(self.size, color, pos)
            if not self.piece_can_down(self.piece):
                self.playing = False

        if self.piece_can_down(self.piece):
            self.piece.move(DOWN)
        else:
            for cell in self.piece:
                self.board.append((cell, self.piece.color))
            self.piece = None

    def pprint(self):
        '''Pretty print the board.'''
        occupied = {}

        if self.piece:
            for cell in self.piece:
                occupied[cell] = ' C'

        for cell in self.board:
            occupied[cell[0]] = ' O'

        for y in range(self.height + 1):
            print('|', end='')
            for x in range(self.width + 1):
                print(occupied.get((x, y), ' .'), end='')
            print(' |')
        print('--' * self.width)

if __name__ == '__main__':
    t = Tetris()

    for _ in range(3):
        while t.playing:
            t.update()
            t.pprint()
            sleep(0.1)
        t.reset()
