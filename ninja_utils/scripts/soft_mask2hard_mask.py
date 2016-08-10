#!/usr/bin/env python
import click
import re

from ninja_utils.parsers import FASTA


@click.command()
@click.option('-i', '--input', type=click.File('r'))
@click.option('-o', '--output', type=click.File('w'), default='-')
def soft_mask2hard_mask(input, output):
    fasta_gen = FASTA(input)

    for title, seq in fasta_gen.read():
        output.write('>%s\n' % title)
        output.write('%s\n', re.sub('[^a-z]', 'N', seq))

if __name__ == '__main__':
    soft_mask2hard_mask()
