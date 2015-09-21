"""
 0 1 2 3
┌──────► X, columns
│
│
│
▼
Y, rows
"""


class Cell(object):
    __slots__ = ['value', 'x', 'y', 'candidates', 'id']

    def __init__(self, value, x, y, id):
        self.value = value
        self.x = x
        self.y = y
        self.id = id
        self.candidates = set()

    def __hash__(self):
        return hash(self.id)

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


class Board(object):
    def __init__(self, matrix):
        size = int(len(matrix) ** 0.5)
        self.matrix = [
            Cell(matrix[x + y * size], x, y, x + y * size)
            for y in range(size)
            for x in range(size)
        ]

    def __iter__(self):
        return iter(self.matrix)

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


    def display(self):
        """
        Draws a border around squares and creates table that looks like:
        ┌────┬────┐
        │ 9_ │ 3_ │
        │ _2 │ _4 │
        ├────┼────┤
        │ __ │ 9_ │
        │ 3_ │ _2 │
        └────┴────┘
        """
        output = []

        borders = ['─' * (self.square_size + 2)] * self.square_size
        header = '┌{}┐'.format('┬'.join(borders))
        middler = '├{}┤'.format('┼'.join(borders))
        footer = '└{}┘'.format('┴'.join(borders))

        output.append(header)
        for y, row in enumerate(self.rows):
            line = []
            for x, num in enumerate(row):
                line += str(num) if num > 0 else '_'
                if (x + 1) % self.square_size == 0 and 1 < x + 1 < self.size:
                    line.append(' │ ')
            line = '│ {} │'.format(''.join(line))
            output.append(line)
            if (y + 1) % self.square_size == 0 and 1 < y + 1 < self.size:
                output.append(middler)

        output.append(footer)
        return '\n'.join(output)
