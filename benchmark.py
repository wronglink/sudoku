"""
This runs a big dataset of sudokus trough solver and checks if them are
all successfully solved.

For more explicit results run:

py.test -v benchmark.py
"""

import pytest
from sudoku.board import Board
from sudoku.rules import RuleHandler
from sudoku.solvers import BacktrackingSolver


matrixes = []
with open('data/problems.txt') as f:
    for line in f:
        matrix = [int(i) for i in line.replace('.', '0').strip()]
        matrixes.append(matrix)


@pytest.fixture(params=matrixes)
def board(request):
    return Board(request.param)

@pytest.fixture
def solver():
    return BacktrackingSolver(RuleHandler())


@pytest.mark.benchmark
def test_solver(board, solver):
    solution = next(solver.solve(board))
    assert all(not cell.is_empty for cell in solution)
