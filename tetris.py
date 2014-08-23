from piece import *
from time import sleep

BG_COLOR = (0, 0, 0)

PIECE_COLORS = {
    'RED': (255, 0, 0),
    'GREEN': (0, 255, 0),
    'BLUE': (0, 0, 255),
    'YELLOW': (255, 255, 50),
    'CYAN': (50, 255, 255),
    'MAGENTA': (255, 50, 255),
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

    def __init__(self, size=4, width=WIDTH, height=HEIGHT):
        '''Init with a optional size parameter for the size of each piece.'''

        self.size = size
        self.width = width - 1
        self.height = height - 1
        self.reset()

    def reset(self):
        '''Restart the game.'''
        self.board = {}
        self.piece = None
        self.next_move = None
        self.speed = INITIAL_SPEED
        self.timer = 1000/self.speed
        self.lines = 0

    def get_board(self):
        '''Return a copy of the current board with the current piece in it.'''
        board = {}
        for cell in self.board:
            board[cell] = self.board[cell]

        if self.piece:
            for cell in self.piece:
                board[cell] = self.piece.color
        return board

    def is_legal(self, piece):
        ''' Checks if the piece can be legally placed in self's board'''
        for cell in piece:
            if cell[1] > self.height:
                return False
            if cell[0] < 0 or cell[0] > self.width:
                return False
            if cell in self.board:
                return False
        return True

    def piece_can_move(self, piece, dir):
        '''  Returh True if the given piece can go down without leaving the
            Board or coliding with another piece.'''
        new_piece = piece.copy()
        new_piece.move(dir)
        return self.is_legal(new_piece)

    def rotate_piece(self, piece, rotate):
        '''
        rotates the  given piece if legal.
        negative for cw rotation and positive for ccw rotation
        '''
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

    def score_lines(self):
        ''' Scores the complete lines on the board.'''
        score = 0
        complete_lines = []

        for y in range(self.height + 1):
            if all([(x, y) in self.board for x in range(self.width + 1)]):
                score += 1
                complete_lines.append(y)

        for line in complete_lines:
            self.remove_line(line)

        return score

    def remove_line(self, line):
        ''' Remove line from the board, dropping all highers lines.'''
        new_board = {}
        for cell in list(self.board.keys()):
            if cell[1] > line:
                new_board[cell] = self.board[cell]
            if cell[1] < line:
                new_board[Vector((cell[0], cell[1] + 1))] = self.board[cell]
        self.board = new_board

    def update(self, dt, move=None, rotate=0):
        '''
        Move the game one step forward.
        dt is the time passed since last call
        move is a direction for the piece to move
        rotate rotates the piece, negative for cw and positive for ccw
        '''
        if not self.piece:
            color = choice(tuple(PIECE_COLORS.values()))
            pos = Vector((self.width // 2, -1))
            self.piece = Piece.Random(self.size, color, pos)
            if not self.piece_can_move(self.piece, DOWN):
                return False

        if move and self.piece_can_move(self.piece, move):
            self.piece.move(move)

        if rotate:
            self.rotate_piece(self.piece, rotate)

        self.timer -= dt
        if self.timer > 0:
            return True

        self.timer += 1000/self.speed

        if self.piece_can_move(self.piece, DOWN):
            self.piece.move(DOWN)
        else:
            for cell in self.piece:
                self.board[cell] = self.piece.color
            self.piece = None

        self.lines += self.score_lines()
        self.speed += self.lines * SPEED_INCREMENT

        return True

    def pprint(self):
        '''Pretty print the board.'''
        occupied = {}

        if self.piece:
            for cell in self.piece:
                occupied[cell] = ' C'

        for cell in self.board:
            occupied[cell] = ' {}'.format(self.board[cell])

        for y in range(self.height + 1):
            print('|', end='')
            for x in range(self.width + 1):
                print(occupied.get((x, y), ' .'), end='')
            print(' |')
        print('--' * self.width * 2)

if __name__ == '__main__':
    t = Tetris(2, 3, 20)
    # t.board = {(22, 0): 1, (22, 1): 1, (21, 0): 1, (21, 1): 1, (21, 2): 2}
    # t.score_lines()
    # t.width = 2
    # t.height = 4
    # t.board = {(0, 3): 1, (1, 3): 1, (1, 2): 1}
    # t.update(10000)
    # t.pprint()

    count = 0
    while True:
        t.update(300, move=Vector((choice((0, 1, -1)), 0)), rotate=choice((-1, 0, 0, 0, 0, 0, 0, 0, 1)))
        print(t.board)
        sleep(0.3)
    t.pprint()
    print(t.lines, count)
