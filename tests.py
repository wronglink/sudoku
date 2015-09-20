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
        column0 = [9, 0, 0, 0, 0, 7, 0, 0, 3]
        columns = list(self.board.columns)
        assert 9 == len(columns)
        assert column0 == columns[0]

    def test_rows(self):
        row0 = [9, 0, 0, 0, 8, 0, 3, 0, 0]
        rows = list(self.board.rows)
        assert 9 == len(rows)
        assert row0 == rows[0]

    def test_squares(self):
        square00 = [9, 0, 0,
                    0, 0, 0,
                    0, 2, 0]
        squares = list(self.board.squares)
        assert 9 == len(squares)
        assert square00 == squares[0]

    def get_square_by_cell(self):
        square00 = [9, 0, 0,
                    0, 0, 0,
                    0, 2, 0]

        square22 = [8, 0, 3,
                    0, 0, 0,
                    0, 0, 0]

        assert square00 == self.board.get_square_by_cell(2, 2)
        assert square22 == self.board.get_square_by_cell(7, 8)


    def test_display(self):
        expected = """\
┌─────┬─────┬─────┐
│ 9__ │ _8_ │ 3__ │
│ ___ │ 25_ │ 7__ │
│ _2_ │ 3__ │ __4 │
├─────┼─────┼─────┤
│ _94 │ ___ │ ___ │
│ ___ │ 73_ │ 56_ │
│ 7_5 │ _6_ │ 4__ │
├─────┼─────┼─────┤
│ __7 │ 8_3 │ 9__ │
│ __1 │ ___ │ __3 │
│ 3__ │ ___ │ __2 │
└─────┴─────┴─────┘"""
        assert expected == self.board.display()
