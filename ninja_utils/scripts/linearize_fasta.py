#!/usr/bin/env python
import click
import sys

@click.command()
@click.option('-i', '--input', type=click.File('rb'), default='-')
@click.option('-o', '--output', type=click.File('wb'), default='-')
def linearize_fasta(input, output):
    output.write(next(input))
    for line in input:
            if line[0] == b'>':
                    output.write(b'\n' + line)
            else:
                    output.write(line[:-2])
    output.write(b'\n')

if __name__ == '__main__':
    linearize_fasta()