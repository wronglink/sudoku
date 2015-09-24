from unittest import TestCase
from sudoku.board import Cell, Board
from sudoku.parsers import TextParser, JSONParser, ParseError
from sudoku.rules import (RuleHandler, unique_in_row,
                          unique_in_column, unique_in_square)
from sudoku.solvers import BacktrackingSolver


class TestCell(TestCase):
    def test_cell(self):
        assert 1 == Cell(1, 0, 5)
        assert 1 != Cell(2, 0, 5)
        assert Cell(2, 0, 5) == Cell(2, 2, 5)
        assert Cell(1, 0, 5) != Cell(2, 2, 5)


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


class TestRulesHandler(TestCase):
    def setUp(self):
        self.matrix = [
            1, 2, 0, 4,
            3, 4, 0, 0,
            2, 1, 0, 4,
            4, 3, 4, 3,
        ]
        self.board = Board(self.matrix)
        self.rules = RuleHandler()

    def test_rules(self):
        cell = self.board.get_cell(1, 1)
        assert self.rules.is_valid(self.board, cell)
        cell = self.board.get_cell(1, 2)
        assert self.rules.is_valid(self.board, cell)
        cell = self.board.get_cell(2, 3)
        assert not self.rules.is_valid(self.board, cell)


def is_solved(board):
    return all(not cell.is_empty for cell in board)


class TestBacktrackingSolver(TestCase):
    def init_solver(self, matrix):
        self.puzzle = Board(matrix)
        self.rules = RuleHandler()
        self.solver = BacktrackingSolver(self.rules)

    def make_matrix(self, matrix):
        return [int(i) for i in matrix.replace('_', '0').split()]

    def test_reduce_candidates(self):
        matrix = self.make_matrix('''
            3 4 1 2
            _ 2 3 _
            _ 3 _ _
            _ _ 4 3''')
        self.init_solver(matrix)
        solution = next(self.solver.solve(self.puzzle))
        cell = solution.get_cell(0, 1)
        assert 1 == cell
        cell = solution.get_cell(0, 2)
        assert 4 == cell

    def test_solve_simple_one_cycle(self):
        matrix = self.make_matrix('''
            3 4 1 2
            _ 2 3 _
            _ 3 2 1
            2 1 4 3''')
        expected = self.make_matrix('''
            3 4 1 2
            1 2 3 4
            4 3 2 1
            2 1 4 3''')
        self.init_solver(matrix)
        solution = next(self.solver.solve(self.puzzle))
        assert is_solved(solution)
        assert expected == solution.matrix

    def test_solve_simple_two_cycles(self):
        matrix = self.make_matrix('''
            _ 4 _ 2
            _ 2 3 _
            _ 3 2 1
            2 1 4 3''')
        expected = self.make_matrix('''
            3 4 1 2
            1 2 3 4
            4 3 2 1
            2 1 4 3''')
        self.init_solver(matrix)
        solution = next(self.solver.solve(self.puzzle))
        assert is_solved(solution)
        assert expected == solution.matrix

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
        solution = next(self.solver.solve(self.puzzle))
        assert is_solved(solution)
        assert solution.matrix in [solution1, solution2]

    def test_solve_many_iterations(self):
        matrix = self.make_matrix('''
            3 _ _ _
            _ _ _ _
            _ _ _ _
            _ _ _ 3''')

        self.init_solver(matrix)
        solution = next(self.solver.solve(self.puzzle))
        assert is_solved(solution)

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
        iterator = iter(self.solver.solve(self.puzzle))
        solution1 = next(iterator)
        assert is_solved(solution1)
        solution2 = next(iterator)
        assert is_solved(solution2)
        assert solution1.matrix != solution2.matrix


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

    def test_loads_wrong_size_exception(self):
        matrix_string = '3 1  4 2 4 _  * 1'
        self.assertRaises(ParseError, self.parser.loads, matrix_string)

    def test_loads_wrong_values_exception(self):
        matrix_string = '''
            3 6  4 7
            4 _  * 1

            1 _  2 4
            2 5  . 3
        '''
        self.assertRaises(ParseError, self.parser.loads, matrix_string)

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
