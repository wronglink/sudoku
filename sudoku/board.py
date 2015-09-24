class Cell(object):
    __slots__ = ['value', 'x', 'y']

    def __init__(self, value, x, y):
        self.value = value
        self.x = x
        self.y = y

    def __hash__(self):
        return hash(self.coords)

    def __eq__(self, other):
        return self.value == other

    def __lt__(self, other):
        return self.value < other

    def __gt__(self, other):
        return self.value > other

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return "<Cell: {} [{}, {}]>".format(self.value, self.x, self.y)

    @property
    def coords(self):
        return self.x, self.y

    @property
    def is_empty(self):
        return self.value == 0


class Board(object):
    def __init__(self, matrix):
        size = int(len(matrix) ** 0.5)
        self.matrix = [
            Cell(matrix[x + y * size], x, y)
            for y in range(size)
            for x in range(size)
        ]

    def __iter__(self):
        return iter(self.matrix)

    def __getitem__(self, key):
        if isinstance(key, slice):
            return self.get_cell(key.start, key.stop)
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
        Returns cell by x, y board coordinates.
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
        Returns square by its x, y coordinates inside board.
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

    def get_square_by_cell(self, x, y):
        """
        Returns square containing cell with x, y coordinates.
        """
        return self.get_square(x // self.square_size, y // self.square_size)

