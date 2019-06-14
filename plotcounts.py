#!/usr/bin/env python
""" plotcounts.py code to plot word counts for the make_novice lesson
"""

import sys
from collections import Sequence
import numpy as np
import matplotlib.pyplot as plt

from countwords import load_word_counts


def plot_word_counts(counts, limit=10):
    """
    Given a list of (word, count, percentage) tuples, plot the counts as a
    histogram. Only the first limit tuples are plotted.
    """
    limited_counts = counts[0:limit]
    word_data = [word for (word, _, _) in limited_counts]
    count_data = [count for (_, count, _) in limited_counts]
    position = np.arange(len(word_data))
    width = 1.0
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)
    ax.set_xticks(position)
    ax.set_xticklabels(word_data)
    plt.bar(position, count_data, width, color='b')
    plt.title("Word Counts")
    ax.set_ylabel("Counts")
    ax.set_xlabel("Word")
    return fig


def typeset_labels(labels=None, gap=5):
    """
    Given a list of labels, create a new list of labels such that each label
    is right-padded by spaces so that every label has the same width, then
    is further right padded by ' ' * gap.
    """
    if not isinstance(labels, Sequence):
        labels = list(range(labels))
    labels = [str(i) for i in labels]
    label_lens = [len(s) for s in labels]
    label_width = max(label_lens)
    output = []
    for label in labels:
        label_string = label + ' ' * (label_width - len(label)) + (' ' * gap)
        output.append(label_string)
    assert len(set(len(s) for s in output)) == 1  # Check all have same length.
    return output


def get_ascii_bars(values, truncate=True, maxlen=10, symbol='#'):
    """
    Given a list of values, create a list of strings of symbols, where each
    strings contains N symbols where N = ()(value / minimum) /
    (maximum - minimum)) * (maxlen / len(symbol)).
    """
    maximum = max(values)
    if truncate:
        minimum = min(values) - 1
    else:
        minimum = 0

    # Type conversion to floats is required for compatibility with python 2,
    # because it doesn't do integer division correctly (it does floor divison
    # for integers).
    value_range = float(maximum - minimum)
    prop_values = [(float(value - minimum) / value_range) for value in values]

    # Type conversion to int required for compatibility with python 2
    biggest_bar = symbol * int(round(maxlen / len(symbol)))
    bars = [biggest_bar[:int(round(prop * len(biggest_bar)))]
            for prop in prop_values]

    return bars


def plot_ascii_bars(values, labels=None, screenwidth=80, gap=2, truncate=True):
    """
    Given a list of values and labels, create right-padded labels for each
    label and strings of symbols representing the associated values.
    """
    if not labels:
        try:
            values, labels = list(zip(*values))
        except TypeError:
            labels = len(values)
    labels = typeset_labels(labels=labels, gap=gap)
    bars = get_ascii_bars(values, maxlen=screenwidth - gap - len(labels[0]),
                          truncate=truncate)
    return [s + b for s, b in zip(labels, bars)]


def main(argv=None):
    '''Parses command line and calls functions to make specified plot

    '''
    import argparse

    if argv is None:                    # Usual case
        argv = sys.argv[1:]

    # Parse command line
    parser = argparse.ArgumentParser(
        description='Make plots for documents or to view')
    parser.add_argument('--limit', type=int, default=10,
                        help='Limit plot the "limit" most frequent words')
    parser.add_argument('--show', action='store_true',
                        help='Display result on screen')
    parser.add_argument('input_file')
    parser.add_argument(
        'output_file', nargs='?',
        help='if "ascii" make a termina plot.  Otherwise specify "name.pdf"')
    args = parser.parse_args(argv)

    # count words in specified book
    counts = load_word_counts(args.input_file)

    # Print ascii plot to terminal if specified
    if args.output_file == 'ascii':
        words, counts, _ = list(zip(*counts))
        for line in plot_ascii_bars(counts[:args.limit], words[:args.limit],
                                    truncate=False):
            print(line)
        return 0

    # Create matplotlib fig object
    fig = plot_word_counts(counts, args.limit)

    # Display if specfied
    if args.show:
        plt.show()

    # Write pdf file if specified
    if args.output_file and args.output_file.find('.pdf') > 0:
        fig.savefig(args.output_file)

    return 0

if __name__ == "__main__":
    sys.exit(main())
