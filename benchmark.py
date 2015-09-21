"""
This runs a big dataset of sudokus trough solver and checks if them are
all successfully solved.

For more explicit results run:

py.test -v benchmark.py
"""

import pytest
from sudoku.board import Board
from sudoku.rules import RuleHandler
from sudoku.solver import BacktrackingSolver


matrixes = []
with open('data/problems.txt') as f:
    for line in f:
        matrix = [int(i) for i in line.replace('.', '0').strip()]
        matrixes.append(matrix)


@pytest.fixture(params=matrixes)
def matrix(request):
    return request.param


@pytest.fixture
def solver(matrix):
    board = Board(matrix)
    rule_handler = RuleHandler()
    return BacktrackingSolver(board, rule_handler)


@pytest.mark.benchmark
def test_solver(solver):
    solver.solve()
    assert solver.solved()
