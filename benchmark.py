"""
This runs a big dataset of sudokus trough solver and checks if them are
all successfully solved.

For more explicit results run:

py.test -v benchmark.py
"""

import pytest
from sudoku.board import Board
from sudoku.rules import RulesHolder
from sudoku.solver import Solver


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
    rules_holder = RulesHolder()
    return Solver(board, rules_holder)


@pytest.mark.benchmark
def test_solver(solver):
    solver.solve()
    assert solver.solved()
