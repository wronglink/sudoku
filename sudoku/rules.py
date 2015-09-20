def unique_in_row(board, x, y):
    value = board[x:y]
    return list(board[:y]).count(value) < 2


def unique_in_column(board, x, y):
    value = board[x:y]
    return list(board[x:]).count(value) < 2


def unique_in_square(board, x, y):
    value = board[x:y]
    return board.get_square_by_cell(x, y).count(value) < 2


class RuleHolder(object):
    default_rules = [unique_in_row, unique_in_column, unique_in_square]

    def __init__(self, board, rules=None):
        self.board = board
        self.rules = []
        self.rules += self.default_rules if rules is None else rules

    def add_rule(self, rule):
        self.rules.append(rule)

    def is_valid(self, x, y):
        return all(rule(self.board, x, y) for rule in self.rules)
