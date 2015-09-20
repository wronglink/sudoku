"""
 0 1 2 3
┌──────► X, columns
│
│
│
▼
Y, rows
"""


class Board(object):
    def __init__(self, matrix):
        self.matrix = matrix

    def __iter__(self):
        return iter(self.matrix)

    def __getitem__(self, key):
        """
        """
        if isinstance(key, slice):
            # [:]
            if key.start is None and key.stop is None:
                raise ValueError('Either collumn or row must be specified')
            # [x:y]
            if key.start is not None and key.stop is not None:
                return self.get_cell(key.start, key.stop)
            # [column:]
            elif key.start is not None:
                return self.get_column(key.start)
            # [:row]
            elif key.stop is not None:
                return self.get_row(key.stop)
        else:
            return self.matrix[key]

    @property
    def size(self):
        return int(len(self.matrix) ** 0.5)

    @property
    def square_size(self):
        return int(len(self.matrix) ** 0.25)

    def get_cell(self, x, y):
        """
        Returns cell value by x, y board coordinates.
        """
        return self.matrix[self.size * y + x]

    @property
    def rows(self):
        """
        Returns generator for every board row.
        """
        return (self.get_row(n) for n in range(self.size))

    def get_row(self, n):
        """
        Returns n-th row
        """
        return self.matrix[self.size * n:self.size * (n + 1)]

    @property
    def columns(self):
        """
        Returns generator for every board column.
        """
        return (self.get_column(n) for n in range(self.size))

    def get_column(self, n):
        """
        Returns n-th column
        """
        return self.matrix[n::self.size]

    @property
    def squares(self):
        """
        Returns generator for every board square.
        """
        for y in range(self.square_size):
            for x in range(self.square_size):
                yield self.get_square(x, y)

    def get_square(self, x, y):
        """
        Retunes n-th square.
        x and y are the coordinates of square.
        ┌─────┬─────┐
        │ 0,0 │ 1,0 │
        ├─────┼─────┤
        │ 0,1 │ 1,1 │
        └─────┴─────┘
        """
        square = []
        _x = self.square_size * x
        _y = self.square_size * y
        offset = self.size * _y + _x
        for i in range(self.square_size):
            square += self.matrix[offset:offset + self.square_size]
            offset += self.size
        return square
