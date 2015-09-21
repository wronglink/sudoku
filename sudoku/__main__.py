import argparse
import os.path
from sudoku.rules import RuleHandler
from sudoku.solver import NoSolutionError, BacktrackingSolver
from sudoku.parsers import PARSER_FILE_EXT_MAPPING

parser = argparse.ArgumentParser(description='Console Sudoku solver')

parser.add_argument('infile', help='Input file',
                    type=argparse.FileType('r'))
parser.add_argument('outfile', help='Output file',
                    type=argparse.FileType('w'))
parser.add_argument('--display', action='store_true',
                    help='Display board before and after solution')


if __name__ == '__main__':
    args = parser.parse_args()

    _, infile_ext = os.path.splitext(args.infile.name)
    if infile_ext not in PARSER_FILE_EXT_MAPPING:
        print('Unknown file extension: {}'.format(args.infile.name))
    _, outfile_ext = os.path.splitext(args.outfile.name)
    if outfile_ext not in PARSER_FILE_EXT_MAPPING:
        print('Unknown file extension: {}'.format(args.outfile.name))

    infile_parser = PARSER_FILE_EXT_MAPPING[infile_ext]()
    outfile_parser = PARSER_FILE_EXT_MAPPING[outfile_ext]()

    board = infile_parser.loads(args.infile.read())
    rule_handler = RuleHandler()
    solver = BacktrackingSolver(board, rule_handler)

    if args.display:
        print('Puzzle:')
        print(board.display())

    try:
        solved_board = solver.solve()
    except NoSolutionError as e:
        print('No solution could be found.')
        exit()

    if args.display:
        print('Solution:')
        print(solved_board.display())
    else:
        print('Puzzle solved.')

    args.outfile.write(outfile_parser.dumps(solved_board))
