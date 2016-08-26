#!/usr/bin/env python
import click
import re

from ninja_utils.parsers import FASTA


@click.command()
@click.option('-i', '--input', type=click.File('r'), default='-')
@click.option('-t', '--threshold', type=click.FLOAT, default=.6)
@click.option('-o', '--output', type=click.File('w'), default='-')
def filter_dusted_fasta(input, threshold, output):
    fasta_gen = FASTA(input)

    for title, seq in fasta_gen.read():
        seq = re.sub('[^A-Z]', 'N', seq)
        hits = sum(1.0 for i in seq if not i == 'N')
        if len(seq) and hits and hits/len(seq) > threshold:
            output.write('>%s\n' % title)
            output.write('%s\n' % re.sub('[^A-Z]', 'N', seq))

if __name__ == '__main__':
    filter_dusted_fasta()
