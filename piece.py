from random import choice
from utils import *

UP = Vector((0, -1))
DOWN = Vector((0, 1))
LEFT = Vector((-1, 0))
RIGHT = Vector((1, 0))


class Piece(object):

    '''
    Represents a Piece as a set of Vectors, and a color.

    '''

    def __init__(self, cells, color, pos=(0, 0)):
        self.cells = cells
        self.color = color
        self.dimensions = max(len(cell) for cell in cells)
        self.pos = pos

    def __len__(self):
        return len(self.cells)

    def __iter__(self):
        return iter(self.cells)

    def __str__(self):
        res = 'Piece:'
        for cell in self:
            res += str(cell)
        return res

    @classmethod
    def Random(cls, size, color, pos=(0, 0)):
        '''creates a random piece of given size and color'''
        cells = Piece.__generate_piece(size)
        return cls(cells, color, pos)

    @staticmethod
    def __generate_piece(size):
        '''Returns a list of Vectors for a piece of given size'''
        cells = set()
        loc = Vector((0, 0))

        cells.add(loc)
        dirs = (UP, LEFT, DOWN, RIGHT)

        while len(cells) < size:
            #Generate from the last position
            cell = choice(tuple(cells))
            direction = choice(dirs)
            loc = cell + direction
            cells.add(loc)

        return cells

    def __normalize(self):
        '''Normalize the shape's center around (0, 0).'''
        sums = [0 for n in range(self.dimensions)]

        for cell in self.cells:
            # Get the total Value of all cells.
            for d, value in enumerate(cell):
                sums[d] += value

            # Calculate the avarage (rounded) and move all the
            # cells in the oposite direction accordingly
        vec = Vector(round(-sum/len(self)) for sum in sums)

        normalized_cells = set()
        for cell in self:
            normalized_cells.add(cell + vec)

        self.cells = normalized_cells

    def move(self, direction):
        self.pos += direction

    def rotate_cw(self):
        '''Rotate the piece clockwise.'''
        new_cells = set()
        for cell in self:
            new_cells.add(Vector((-cell[1], cell[0])))

        self.cells = new_cells

    def pprint(self, size=6):
        '''Pretty prints the shape on the screen'''

        for y in range(-size//2, size - size//2):
            for x in range(-size//2, size - size//2):

                if (x, y) in self.cells:
                    print('*', end='')
                else:
                    print(' ', end='')
            print()


if __name__ == '__main__':

    for _ in range(10):
        p = Piece.Random(4, 'a')

        for _ in range(4):
            p.rotate_cw()
            print(p)
            p.pprint()
        print('=======================')
