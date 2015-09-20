from unittest import TestCase
from .sudoku import Board


class TestBoard(TestCase):
    def setUp(self):
        self.matrix = [
            9, 0, 0,  0, 8, 0,  3, 0, 0,
            0, 0, 0,  2, 5, 0,  7, 0, 0,
            0, 2, 0,  3, 0, 0,  0, 0, 4,
            0, 9, 4,  0, 0, 0,  0, 0, 0,
            0, 0, 0,  7, 3, 0,  5, 6, 0,
            7, 0, 5,  0, 6, 0,  4, 0, 0,
            0, 0, 7,  8, 0, 3,  9, 0, 0,
            0, 0, 1,  0, 0, 0,  0, 0, 3,
            3, 0, 0,  0, 0, 0,  0, 0, 2,
        ]

        self.board = Board(self.matrix)

    def test_slicing(self):
        column = [9, 0, 0, 0, 0, 7, 0, 0, 3]
        row = [9, 0, 0, 0, 8, 0, 3, 0, 0]
        assert column == self.board[0:]
        assert row == self.board[:0]
        assert 9 == self.board[0:0]
        assert 3 == self.board[0:8]
        assert 2 == self.board[8:8]

    def test_columns(self):
        column = [9, 0, 0, 0, 0, 7, 0, 0, 3]
        columns = list(self.board.columns)
        assert 9 == len(columns)
        assert column == columns[0]

    def test_rows(self):
        row = [9, 0, 0, 0, 8, 0, 3, 0, 0]
        rows = list(self.board.rows)
        assert 9 == len(rows)
        assert row == rows[0]

    def test_squares(self):
        square = [9, 0, 0,
                  0, 0, 0,
                  0, 2, 0]
        squares = list(self.board.squares)
        assert 9 == len(squares)
        assert square == squares[0]
