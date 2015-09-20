class NoSolutionError(Exception):
    pass


class Solver(object):
    def __init__(self, board, rules_holder):
        self.board = board
        self.rules_holder = rules_holder

    def solve(self):
        while self.reduce_candidates():
            continue
        if not self.solved():
            pass
        return self.board

    def solved(self):
        return all(i != 0 for i in self.board)

    def reduce_candidates(self):
        """
        Iterate cells and set their candidate values.
        If it's the only one candidate left use it for cell value.
        Returns True if cell values changed, False if not.
        """
        changed = False
        for cell in self.board:
            if cell == 0:
                bad_candidates = set()

                # try candidates and remove the bad ones
                for candidate in cell.candidates:
                    cell.value = candidate
                    if not self.rules_holder.is_valid(cell):
                        bad_candidates.add(candidate)
                    cell.value = 0
                cell.candidates -= bad_candidates

                # Use candidate if it's the only one
                if len(cell.candidates) == 1:
                    changed = True
                    cell.value = cell.candidates.pop()

            if cell == 0 and not cell.candidates:
                raise NoSolutionError(
                    'No candidate found for cell {}'.format(repr(cell)))

        return changed
