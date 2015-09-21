def unique_in_row(board, cell):
    row = board.get_row(cell.y)
    return row.count(cell) < 2


def unique_in_column(board, cell):
    column = board.get_column(cell.x)
    return column.count(cell) < 2


def unique_in_square(board, cell):
    square = board.get_square_by_cell(cell.x, cell.y)
    return square.count(cell) < 2


class RuleHandler(object):
    """
    Object that handles game rules and can tell that specific cell
    doesn't break rules on the board.
    """
    default_rules = [unique_in_row, unique_in_column, unique_in_square]

    def __init__(self, rules=None):
        self.rules = []
        for rule in rules or self.default_rules:
            self.add_rule(rule)

    def add_rule(self, rule):
        """
        Adds game rule. The `rule` must be a callable, that takes
        2 arguments: `board` and `cell`. Must return True if cell
        fits board, False otherwise.
        """
        self.rules.append(rule)

    def is_valid(self, board, cell):
        """
        Validates that specified cell fits all defined rules
        """
        return all(rule(board, cell) for rule in self.rules)
