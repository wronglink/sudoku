from unittest import TestCase
from sudoku.board import Cell, Board
from sudoku.rules import (RuleHolder, unique_in_row,
                          unique_in_column, unique_in_square)


class TestCell(TestCase):
    def test_cell(self):
        assert 1 == Cell(1, 0, 5, 9)
        assert 1 != Cell(2, 0, 5, 9)
        assert Cell(2, 0, 5, 9) == Cell(2, 2, 5, 9)
        assert Cell(1, 0, 5, 9) != Cell(2, 2, 5, 9)


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
        self.row0 = [9, 0, 0, 0, 8, 0, 3, 0, 0]
        self.column0 = [9, 0, 0, 0, 0, 7, 0, 0, 3]

    def test_get_cell(self):
        assert 9 == self.board.get_cell(0, 0)
        assert 3 == self.board.get_cell(0, 8)
        assert 2 == self.board.get_cell(8, 8)

    def test_get_column(self):
        assert self.column0 == self.board.get_column(0)

    def test_columns(self):
        columns = list(self.board.columns)
        assert 9 == len(columns)
        assert self.column0 == columns[0]

    def test_get_row(self):
        assert self.row0 == self.board.get_row(0)

    def test_rows(self):
        rows = list(self.board.rows)
        assert 9 == len(rows)
        assert self.row0 == rows[0]

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


class TestRules(TestCase):
    def setUp(self):
        self.matrix = [
            1, 2, 0, 4,
            3, 4, 0, 0,
            2, 1, 0, 4,
            4, 4, 1, 3,
        ]
        self.board = Board(self.matrix)

    def test_unique_in_row(self):
        cell = self.board.get_cell(1, 0)
        assert unique_in_row(self.board, cell)
        cell = self.board.get_cell(1, 3)
        assert not unique_in_row(self.board, cell)

    def test_unique_in_column(self):
        cell = self.board.get_cell(0, 1)
        assert unique_in_column(self.board, cell)
        cell = self.board.get_cell(3, 0)
        assert not unique_in_column(self.board, cell)

    def test_unique_in_square(self):
        cell = self.board.get_cell(1, 1)
        assert unique_in_square(self.board, cell)
        cell = self.board.get_cell(0, 3)
        assert not unique_in_square(self.board, cell)


class TestRuleHolder(TestCase):
    def setUp(self):
        self.matrix = [
            1, 2, 0, 4,
            3, 4, 0, 0,
            2, 1, 0, 4,
            4, 3, 4, 3,
        ]
        self.board = Board(self.matrix)
        self.rule_holder = RuleHolder(self.board)

    def test_rule_holder(self):
        cell = self.board.get_cell(1, 1)
        assert self.rule_holder.is_valid(cell)
        cell = self.board.get_cell(1, 2)
        assert self.rule_holder.is_valid(cell)
        cell = self.board.get_cell(2, 3)
        assert not self.rule_holder.is_valid(cell)
