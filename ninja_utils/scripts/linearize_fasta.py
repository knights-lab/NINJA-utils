#!/usr/bin/env python
import click
import sys

@click.command()
@click.option('-i', '--input', type=click.File('r'), default='-')
@click.option('-o', '--output', type=click.File('w'), default='-')
def linearize_fasta(input, output):
    output.write(next(input).rstrip() + '\n')
    for line in input:
        if line[0] == '>':
                output.write('\n' + line)
        else:
                output.write(line.rstrip())
    output.write('\n')

if __name__ == '__main__':
    linearize_fasta()