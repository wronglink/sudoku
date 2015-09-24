from contextlib import contextmanager
import copy


@contextmanager
def tmp_value(cell, value):
    """
    Sets cell value inside context.
    """
    cell.value = value
    yield
    cell.value = 0


class BacktrackingSolver(object):
    """
    This solver uses Backtrack algorithm and several heuristics to solve
    the sudoku puzzle.

    The common algorithms fits these steps:

    1.  Make predictions for every unsolved cell by finding candidates.
        A proper candidate follows all rules defined by rule_handler.
        If we can't find any proper candidate for any cell, we assume
        that puzzle could not be solved.
    2.  Find every obvious situation, when cell has only one candidate
        and fill it with the candidate.
    3.  Repeat 1, 2 in cycle until there is now candidates changes and
        no obvious cell values left.
    4.  Find first cell with several candidates and try to fill it with first
        one. Try steps 1-3. There are 3 situations available:
        1.  The board is solved. Then return the current board layout as
            the solution.
        2.  The board layout became unsolvable. Undo all steps till last
            prediction in step 4, recalculate cell's candidates, mark
            selected candidate as inappropriate and try anther one.
        3.  The board is neither solved nor unsolvable. Repeat step 4.

    Finally we would find a solution or find out that it does not exist.
    """
    def __init__(self, rules):
        self.rules = rules

    def solve(self, puzzle, candidates=None):
        """
        Returns generator for every puzzle solution.
        """
        solution = copy.deepcopy(puzzle)
        candidates = copy.deepcopy(candidates) or {}
        default_candidates = range(1, solution.size + 1)

        while True:
            has_changed = False
            for cell in (c for c in solution if c.is_empty):
                bad_candidates = set()
                if cell not in candidates:
                    candidates[cell] = set(default_candidates)
                for candidate in candidates[cell]:
                    with tmp_value(cell, candidate):
                        if not self.rules.is_valid(solution, cell):
                            bad_candidates.add(candidate)
                candidates[cell] -= bad_candidates
                if len(candidates[cell]) == 1:
                    cell.value = candidates[cell].pop()
                    has_changed = True
                elif cell.is_empty and not candidates[cell]:
                    raise StopIteration
            if not has_changed:
                break

        for cell in (c for c in solution if c.is_empty):
            for candidate in candidates[cell]:
                with tmp_value(cell, candidate):
                    yield from self.solve(solution, candidates)
            raise StopIteration
        yield solution
