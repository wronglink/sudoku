def unique_in_row(board, cell):
    row = board.get_row(cell.y)
    return row.count(cell) < 2


def unique_in_column(board, cell):
    column = board.get_column(cell.x)
    return column.count(cell) < 2


def unique_in_square(board, cell):
    square = board.get_square_by_cell(cell.x, cell.y)
    return square.count(cell) < 2


class RulesHolder(object):
    default_rules = [unique_in_row, unique_in_column, unique_in_square]

    def __init__(self, rules=None):
        self.rules = []
        self.rules += self.default_rules if rules is None else rules

    def add_rule(self, rule):
        self.rules.append(rule)

    def is_valid(self, board, cell):
        return all(rule(board, cell) for rule in self.rules)
