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

INITIAL_SPEED = 5
SPEED_INCREMENT = 0.1


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
        self.next_move = None
        self.speed = INITIAL_SPEED
        self.timer = 1000/self.speed
        self.drop_count = 0

    def is_legal(self, piece):
        ''' Checks if the piece can be legally placed in self's board'''
        for cell in piece:
            if cell[1] > self.height:
                return False
            if cell[0] < 0 or cell[0] > self.width:
                return False
            if len([coor for coor in self.board if cell in coor]) > 0:
                return False
        return True

    def piece_can_move(self, piece, dir):
        '''  Returh True if the given piece can go down without leaving the
            Board or coliding with another piece.'''
        new_piece = piece.copy()
        new_piece.move(dir)
        return self.is_legal(new_piece)

    def rotate_piece(self, piece, rotate):
        new_piece = piece.copy()
        if rotate < 0:
            new_piece.rotate_cw()
        else:
            new_piece.rotate_ccw()

        if self.is_legal(new_piece):
            if rotate < 0:
                piece.rotate_cw()
            else:
                piece.rotate_ccw()

    def update(self, dt, move=None, rotate=0):
        '''
        Move the game one step forward.
        dt is the time passed since last call
        move is a direction for the piece to move
        rotate rotates the piece, negative for cw and positive for ccw
        '''
        if not self.piece:
            color = choice(tuple(PIECE_COLORS.values()))
            pos = Vector((self.width // 2, 0))
            self.piece = Piece.Random(self.size, color, pos)
            if not self.piece_can_move(self.piece, DOWN):
                self.playing = False

        if move and self.piece_can_move(self.piece, move):
            self.piece.move(move)

        if rotate:
            self.rotate_piece(self.piece, rotate)

        self.timer -= dt
        if self.timer > 0:
            return

        self.timer += 1000/self.speed

        if self.piece_can_move(self.piece, DOWN):
            self.piece.move(DOWN)
        else:
            for cell in self.piece:
                self.board.append((cell, self.drop_count))
            self.drop_count = (self.drop_count + 1) % 10
            self.piece = None

    def pprint(self):
        '''Pretty print the board.'''
        occupied = {}

        if self.piece:
            for cell in self.piece:
                occupied[cell] = ' C'

        for cell in self.board:
            occupied[cell[0]] = ' {}'.format(cell[1])

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
            t.update(1000, move=Vector((choice((0, 1, -1)), 0)), rotate=choice((-1, 0, 0, 0, 0, 0, 0, 0, 1)))
            t.pprint()
            sleep(0.1)
        t.reset()
