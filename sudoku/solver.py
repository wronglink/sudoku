class NoSolutionError(Exception):
    """
    Solver can't find any matching solution.
    """
    def __init__(self, message, changed=None):
        super().__init__(message)
        self.changed = changed


class BaseSolver(object):
    """
    Base solver class. Every solver must implement it's own `solve()` method.
    """
    def __init__(self, board, rule_handler):
        self.board = board
        self.rule_handler = rule_handler

    @property
    def unsolved_cells(self):
        for cell in self.board:
            if cell.is_empty:
                yield cell

    def set_unsolved_cells(self, cells):
        """
        Set every specified cell as unsolved.
        """
        for cell in cells:
            cell.value = 0

    def solve(self):
        """
        Solves puzzle or raises `NoSolutionError`.
        """
        raise NotImplementedError

    def solved(self):
        """
        Returns True if all cells are not empty and False otherwise.
        """
        return not any(self.unsolved_cells)

    def reset_candidates(self):
        """
        Sets default cell candidates set to every empty cell.
        """
        for cell in self.unsolved_cells:
            cell.candidates = set(range(1, self.board.size + 1))


class BacktrackingSolver(BaseSolver):
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
    def solve(self):
        if self.solved():
            return self.board
        self.reset_candidates()

        # Try to solve board with obvious values. Track all our
        # changes if our prediction about cell value was wrong.
        changed = set()
        while True:
            try:
                new_changed = self.reduce_candidates()
            except NoSolutionError as e:
                if e.changed:
                    changed |= e.changed
                self.set_unsolved_cells(changed)
                self.reset_candidates()
                raise
            if not new_changed:
                break
            changed |= new_changed

        # If not solved make a prediction and see if we can
        # solve such board in a recursion
        if not self.solved():
            for cell in self.unsolved_cells:
                for candidate in cell.candidates:
                    cell.value = candidate
                    try:
                        return self.solve()
                    except NoSolutionError:
                        cell.value = 0
                        self.set_unsolved_cells(changed)
                        self.reset_candidates()
        return self.board

    def reduce_candidates(self):
        """
        Iterate cells and set their candidate values.
        If it's the only one candidate left use it for cell value.
        Returns a set of cells that values were changed.
        """
        changed = set()
        for cell in self.unsolved_cells:
            bad_candidates = set()

            # Try candidates and remove the bad ones
            for candidate in cell.candidates:
                cell.value = candidate
                if not self.rule_handler.is_valid(self.board, cell):
                    bad_candidates.add(candidate)
                cell.value = 0
            cell.candidates -= bad_candidates

            # Use candidate if it's the only one
            if len(cell.candidates) == 1:
                new_value = cell.candidates.pop()
                changed.add(cell)
                cell.value = new_value

            if cell.is_empty and not cell.candidates:
                raise NoSolutionError(
                    'No candidate found for cell {}'.format(repr(cell)),
                    changed)
        return changed
