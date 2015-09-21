import json
import string
from itertools import chain
from sudoku.board import Board


class BaseParser(object):
    def is_valid_matrix(self, matrix):
        pass

    def is_valid_size(self, matrix):
        size = len(matrix) ** 0.25
        return int(size) == size

    def get_board(self, matrix):
        return Board(matrix)

    def loads(self, s):
        raise NotImplementedError

    def dumps(self, board):
        raise NotImplementedError


class TextParser(BaseParser):
    """
    Loads and dumps sudoku boards in text format:

        53_  _7_  ___           53**7****
        6__  195  ___           6**195***
        _98  ___  _6_           *98****6*
                                8***6***3
        8__  _6_  __3    or     4**8*3**1
        4__  8_3  __1           7***2***6
        7__  _2_  __6           *6****28*
                                ***419**5
        _6_  ___  28_           ****8**79
        ___  419  __5
        ___  _8_  _79

    1. All space-like characters are omitted.
    2. Characters `.`, `_`, `*` are used as blank space and need
       to be filled with solution numbers.
    """
    def __init__(self, free_space_chars='_*.'):
        self.free_space_chars = free_space_chars

    def loads(self, s):
        for char in self.free_space_chars:
            s = s.replace(char, '0')
        for char in string.whitespace:
            s = s.replace(char, '')
        matrix = [int(i) for i in s]
        return self.get_board(matrix)

    def dumps(self, board):
        space_char = self.free_space_chars[0]
        output = []
        for y, row in enumerate(board.rows):
            line = []
            for x, num in enumerate(row):
                line += str(num) if num > 0 else space_char
                if (x + 1) % board.square_size == 0 and 1 < x + 1 < board.size:
                    line.append(' ')
            output.append(''.join(line))
            if (y + 1) % board.square_size == 0 and 1 < y + 1 < board.size:
                output.append('')
        return '\n'.join(output)


class JSONParser(BaseParser):
    """
    Loads and dumps sudoku boards in json format (array of arrays
    for every board row, space blanks indicated by 0):

        [
            [5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9]
        ]
    """
    def loads(self, s):
        matrix = json.loads(s)
        matrix = list(chain(*matrix))
        return self.get_board(matrix)

    def dumps(self, board):
        output = [[cell.value for cell in row] for row in board.rows]
        return json.dumps(output)
