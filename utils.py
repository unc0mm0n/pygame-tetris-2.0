class Vector(tuple):

    '''
    A basic implementation of a Vector as a tuple.
    supports addition and subtraction of vectors, and multiplication
    and division by a scalar.
    '''

    def __repr__(self):
        return 'Vector({0})'.format(tuple(self))

    def __str__(self):
        return str(tuple(self))

    # Basic operations

    def __add__(self, other):
        return Vector(v + w for v, w in zip(self, other))

    def __radd__(self, other):
        return Vector(w + v for v, w in zip(self, other))

    def __sub__(self, other):
        return Vector(v - w for v, w in zip(self, other))

    def __rsub__(self, other):
        return Vector(w - v for v, w in zip(self, other))

    def __mul__(self, s):
        return Vector(v*s for v in self)

    def __rmul__(self, s):
        return Vector(v*s for v in self)

    def __floordiv__(self, s):
        return Vector(v//s for v in self)

    def __rfloordiv__(self, s):
        return Vector(s//v for v in self)

    def __truediv__(self, s):
            return Vector(v/s for v in self)

    def __rtruediv__(self, s):
        return Vector(s/v for v in self)

    def __neg__(self):
        return -1 * self
