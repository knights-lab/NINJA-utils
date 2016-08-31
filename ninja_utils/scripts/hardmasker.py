#!/usr/bin/env python
import click
import os
import tempfile

from ninja_utils.scripts.soft_mask2hard_mask import soft_mask2hard_mask

from ninja_dojo.wrappers import dustmasker


@click.command()
@click.option('-i', '--input', type=click.STRING, default='-')
@click.option('-o', '--output', type=click.STRING, default='-')
def hardmasker(input, output):
    tmpdir = tempfile.mkdtemp()
    predictable_filename = 'temp.fna'

    # Ensure the file is read/write by the creator only
    saved_umask = os.umask(0o0077)

    tf_fasta = os.path.join(tmpdir, predictable_filename)
    try:
        dustmasker(input, tf_fasta)
        soft_mask2hard_mask(tf_fasta, output)
    except IOError as e:
        print('IOError')
    else:
        os.remove(tf_fasta)
    finally:
        os.umask(saved_umask)
        os.rmdir(tmpdir)

if __name__ == '__main__':
    hardmasker()
