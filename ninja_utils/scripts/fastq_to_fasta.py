#!/usr/bin/env python
import argparse
import sys

from ninja_utils.parsers import FASTQ


def make_arg_parser():
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-i', '--input', required=True, help='The input FASTA file')
    parser.add_argument('-o', '--output', help='If nothing is given, then stdout, else write to file')
    return parser

def fastq_to_fasta():
    parser = make_arg_parser()
    args = parser.parse_args()
    with open(args.input) as inf:
        with open(args.output, 'w') if args.output else sys.stdout as outf:
            fastq = FASTQ(inf)
            for header, sequence, qualities in fastq.read():
                outf.write('>%s\n%s\n' % (header, sequence)) 

if __name__ == '__main__':
    fastq_to_fasta()
