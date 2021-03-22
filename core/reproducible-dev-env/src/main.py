import argparse
import sys

from sudoku import SudokuGenerator


def parse_arguments(argv):

    parser = argparse.ArgumentParser(description="description")

    parser.add_argument("-s", "--seed", type=str, default=42)
    parser.add_argument("-l", "--level", type=int, default=50)

    return parser.parse_args()


def main(args):
    print("seed=", args.seed, "level=", args.level)
    sg = SudokuGenerator()
    sg.sudoku_generator(seed=args.seed, level=args.level)
    print(sg.sudoku)


if __name__ == "__main__":

    main(parse_arguments(sys.argv[1:]))
