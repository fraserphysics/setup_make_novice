#!/usr/bin/env python
""" Print a table of the 2 most frequent words in each book
"""

import sys
import argparse

from countwords import load_word_counts

def top_two_word(counts):
    """
    Given a list of (word, count, percentage) tuples,
    return the top two word counts.
    """
    limited_counts = counts[0:2]
    count_data = [count for (_, count, _) in limited_counts]
    return count_data

def main(argv=None):

    if argv is None:                    # Usual case
        argv = sys.argv[1:]

    # Set up a parser and parse the command line arguements
    parser = argparse.ArgumentParser(
        description='Print a table of the 2 most frequent words in each book')
    parser.add_argument('data_files', nargs='*', help='list of data files')
    parser.add_argument('--latex', action='store_true',
                        help='Use LaTeX format for table')
    args = parser.parse_args(argv)

    if args.latex:
        header = 'Book & First & Second & Ratio\\\\ \\hline'
        line_format = '%s & %i & %i & %.2f \\\\'
    else:
        header = "Book\tFirst\tSecond\tRatio"
        line_format = "%s\t%i\t%i\t%.2f"

    print(header)

    # Print the analysis for each book
    for input_file in args.data_files:
        counts = load_word_counts(input_file)
        [first, second] = top_two_word(counts)
        bookname = input_file[:-4]
        print(line_format%(bookname, first, second, float(first)/second))

if __name__ == '__main__':
    sys.exit(main())
