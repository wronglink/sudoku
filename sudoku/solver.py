class NoSolutionError(Exception):
    def __init__(self, message, changed=None):
        super().__init__(message)
        self.changed = changed


class Solver(object):
    def __init__(self, board, rules_holder):
        self.board = board
        self.rules_holder = rules_holder

    @property
    def unsolved_cells(self):
        for cell in self.board:
            if cell == 0:
                yield cell

    def solve(self):
        if self.solved():
            return self.board
        changed = set()
        self.reset_candidates()
        while True:
            try:
                new_changed = self.reduce_candidates()
            except NoSolutionError as e:
                if e.changed:
                    changed |= e.changed
                self.undo_reduce_candidates(changed)
                raise
            if not new_changed:
                break
            changed |= new_changed
        if not self.solved():
            for cell in self.unsolved_cells:
                for candidate in cell.candidates:
                    # print('Try cell {} with {}'.format(repr(cell), candidate))
                    cell.value = candidate
                    # print(self.board.display())
                    try:
                        # print('Go inside!')
                        return self.solve()
                    except NoSolutionError:
                        # print('Try cell {} failed'.format(repr(cell)))
                        cell.value = 0
                        self.undo_reduce_candidates(changed)
                        # print(self.board.display())
        else:
            return self.board
        raise NoSolutionError(":-(")

    def solved(self):
        return not any(self.unsolved_cells)

    def reset_candidates(self):
        for cell in self.unsolved_cells:
            cell.candidates = set(range(1, self.board.size + 1))

    def reduce_candidates(self):
        """
        Iterate cells and set their candidate values.
        If it's the only one candidate left use it for cell value.
        Returns True if cell values changed, False if not.
        """
        changed = set()
        for cell in self.unsolved_cells:
            bad_candidates = set()

            # try candidates and remove the bad ones
            for candidate in cell.candidates:
                cell.value = candidate
                if not self.rules_holder.is_valid(self.board, cell):
                    bad_candidates.add(candidate)
                cell.value = 0
            cell.candidates -= bad_candidates

            # Use candidate if it's the only one
            if len(cell.candidates) == 1:
                new_value = cell.candidates.pop()
                # print('Changed value for cell {} to {}'.format(repr(cell), new_value))
                changed.add(cell)
                cell.value = new_value
                # print(self.board.display())

            if cell == 0 and not cell.candidates:
                # print('Cell {} has no candidates'.format(repr(cell)))
                # print(self.board.display())
                raise NoSolutionError(
                    'No candidate found for cell {}'.format(repr(cell)),
                    changed)
        return changed

    def undo_reduce_candidates(self, cells):
        for cell in cells:
            cell.value = 0
        self.reset_candidates()
