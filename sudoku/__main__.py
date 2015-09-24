import argparse
import os.path
from sudoku.rules import RuleHandler
from sudoku.solvers import BacktrackingSolver
from sudoku.parsers import PARSER_FILE_EXT_MAPPING, ParseError, TextParser

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
    text_parser = TextParser()

    try:
        puzzle = infile_parser.loads(args.infile.read())
    except ParseError as e:
        print(e)
        exit(1)

    rules = RuleHandler()
    solver = BacktrackingSolver(rules)

    if args.display:
        print('Puzzle:')
        print(text_parser.dumps(puzzle))

    try:
        solution = next(solver.solve(puzzle))
    except StopIteration:
        print('No solution could be found.')
        exit(2)

    if args.display:
        print('Solution:')
        print(text_parser.dumps(solution))
    else:
        print('Puzzle solved.')

    args.outfile.write(outfile_parser.dumps(solution))
