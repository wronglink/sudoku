from unittest import TestCase
from sudoku.board import Cell, Board
from sudoku.parsers import TextParser, JSONParser
from sudoku.rules import (RuleHandler, unique_in_row,
                          unique_in_column, unique_in_square)
from sudoku.solver import BacktrackingSolver, NoSolutionError


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
        self.rule_handler = RuleHandler()

    def test_rule_handler(self):
        cell = self.board.get_cell(1, 1)
        assert self.rule_handler.is_valid(self.board, cell)
        cell = self.board.get_cell(1, 2)
        assert self.rule_handler.is_valid(self.board, cell)
        cell = self.board.get_cell(2, 3)
        assert not self.rule_handler.is_valid(self.board, cell)


class TestBacktrackingSolver(TestCase):
    def init_solver(self, matrix):
        self.board = Board(matrix)
        self.rule_handler = RuleHandler()
        self.solver = BacktrackingSolver(self.board, self.rule_handler)

    def make_matrix(self, matrix):
        return [int(i) for i in matrix.replace('_', '0').split()]

    def test_reset_candidates(self):
        matrix = self.make_matrix('''
            3 4 1 2
            _ 2 _ 4
            _ _ _ 1
            2 1 4 _''')
        self.init_solver(matrix)
        self.solver.reset_candidates()
        cell = self.board.get_cell(0, 1)
        assert {1, 2, 3, 4} == cell.candidates
        cell = self.board.get_cell(2, 2)
        assert {1, 2, 3, 4} == cell.candidates

    def test_reduce_candidates(self):
        matrix = self.make_matrix('''
            3 4 1 2
            _ 2 3 _
            _ 3 _ _
            _ _ 4 3''')
        self.init_solver(matrix)
        self.solver.reset_candidates()
        assert self.solver.reduce_candidates()
        cell = self.board.get_cell(0, 1)
        assert 1 == cell
        assert set() == cell.candidates
        cell = self.board.get_cell(0, 2)
        assert cell.is_empty
        assert {2, 4} == cell.candidates

    def test_cant_reduce_candidates(self):
        matrix = self.make_matrix('''
            3 _ _ 2
            _ 2 3 _
            _ 3 2 _
            2 _ _ 3''')
        expected = self.make_matrix('''
            3 _ _ 2
            _ 2 3 _
            _ 3 2 _
            2 _ _ 3''')
        self.init_solver(matrix)
        self.solver.reset_candidates()
        assert not self.solver.reduce_candidates()
        assert expected == self.solver.board.matrix


    def test_reduce_candidates_raises_no_solution(self):
        matrix = self.make_matrix('''
            3 4 1 2
            _ 2 3 4
            2 4 2 4
            1 3 4 3''')
        self.init_solver(matrix)
        self.solver.reset_candidates()
        self.assertRaises(NoSolutionError, self.solver.reduce_candidates)

    def test_solved(self):
        matrix = self.make_matrix('''
            3 4 1 2
            1 2 3 4
            4 3 2 1
            2 1 4 3''')
        self.init_solver(matrix)
        assert self.solver.solved()
        matrix = self.make_matrix('''
            _ 4 1 2
            1 2 3 4
            4 3 2 1
            2 1 4 3''')
        self.init_solver(matrix)
        assert not self.solver.solved()

    def test_solve_simple_one_cycle(self):
        matrix = self.make_matrix('''
            3 4 1 2
            _ 2 3 _
            _ 3 2 1
            2 1 4 3''')
        solution = self.make_matrix('''
            3 4 1 2
            1 2 3 4
            4 3 2 1
            2 1 4 3''')
        self.init_solver(matrix)
        solved_board = self.solver.solve()
        assert self.solver.solved()
        assert solution == solved_board.matrix

    def test_solve_simple_two_cycles(self):
        matrix = self.make_matrix('''
            _ 4 _ 2
            _ 2 3 _
            _ 3 2 1
            2 1 4 3''')
        solution = self.make_matrix('''
            3 4 1 2
            1 2 3 4
            4 3 2 1
            2 1 4 3''')
        self.init_solver(matrix)
        solved_board = self.solver.solve()
        assert self.solver.solved()
        assert solution == solved_board.matrix

    def test_solve_with_iteration(self):
        matrix = self.make_matrix('''
            3 _ _ 2
            _ 2 3 _
            _ 3 2 _
            2 _ _ 3''')
        solution1 = self.make_matrix('''
            3 4 1 2
            1 2 3 4
            4 3 2 1
            2 1 4 3''')
        solution2 = self.make_matrix('''
            3 1 4 2
            4 2 3 1
            1 3 2 4
            2 4 1 3''')

        self.init_solver(matrix)
        solved_board = self.solver.solve()
        assert self.solver.solved()
        assert solved_board.matrix in [solution1, solution2]

    def test_solve_many_iterations(self):
        matrix = self.make_matrix('''
            3 _ _ _
            _ _ _ _
            _ _ _ _
            _ _ _ 3''')

        self.init_solver(matrix)
        self.solver.solve()
        assert self.solver.solved()

    def test_solve_many_iterations3x3(self):
        matrix = self.make_matrix('''
            3 _ _ _ _ _ _ _ _
            _ _ _ _ _ _ _ _ _
            _ _ _ _ _ _ _ _ _
            _ _ _ _ _ _ _ _ _
            _ _ _ _ _ _ _ _ _
            _ _ _ _ _ _ _ _ _
            _ _ _ _ _ _ _ _ _
            _ _ _ _ _ _ _ _ _
            _ _ _ _ _ _ _ _ 3''')

        self.init_solver(matrix)
        self.solver.solve()
        assert self.solver.solved()


class TestTextParser(TestCase):
    def setUp(self):
        self.parser = TextParser()

    def test_loads(self):
        matrix_string = '''
            3 1  4 2
            4 _  * 1

            1 _  2 4
            2 4  . 3
        '''
        matrix_expected = [
            3, 1, 4, 2,
            4, 0, 0, 1,
            1, 0, 2, 4,
            2, 4, 0, 3,
        ]
        board = self.parser.loads(matrix_string)
        assert matrix_expected == board.matrix

    def test_dumps(self):
        matrix_string = '''\
31 42
4_ _1

1_ 24
24 _3'''
        matrix = [
            3, 1, 4, 2,
            4, 0, 0, 1,
            1, 0, 2, 4,
            2, 4, 0, 3,
        ]
        board = Board(matrix)
        dump = self.parser.dumps(board)
        assert matrix_string == dump


class TestJSONParser(TestCase):
    def setUp(self):
        self.parser = JSONParser()

    def test_loads(self):
        matrix_string = '''\
[
    [3, 1, 4, 2],
    [4, 0, 0, 1],
    [1, 0, 2, 4],
    [2, 4, 0, 3]
]'''
        matrix_expected = [
            3, 1, 4, 2,
            4, 0, 0, 1,
            1, 0, 2, 4,
            2, 4, 0, 3,
        ]
        board = self.parser.loads(matrix_string)
        assert matrix_expected == board.matrix

    def test_dumps(self):
        matrix_string = ('[[3, 1, 4, 2], [4, 0, 0, 1], '
                         '[1, 0, 2, 4], [2, 4, 0, 3]]')
        matrix = [
            3, 1, 4, 2,
            4, 0, 0, 1,
            1, 0, 2, 4,
            2, 4, 0, 3,
        ]
        board = Board(matrix)
        dump = self.parser.dumps(board)
        assert matrix_string == dump
