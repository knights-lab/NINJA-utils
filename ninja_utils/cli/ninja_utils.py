import click
from functools import update_wrapper
import os

from ninja_utils.parsers import FASTA, FASTQ2


@click.group(chain=True)
def cli():
    """This script processes a bunch of images through pillow in a unix
    pipe.  One commands feeds into the next.
    Example:
    imagepipe open -i example01.jpg resize -w 128 display
    imagepipe open -i example02.jpg blur save
    """


@cli.resultcallback()
def process_commands(processors):
    """This result callback is invoked with an iterable of all the chained
    subcommands.  As in this example each subcommand returns a function
    we can chain them together to feed one into the other, similar to how
    a pipe on unix works.
    """
    iterator = ()
    for processor in processors:
        iterator = processor(iterator)
    for item in iterator:
        click.echo(item)


def processor(f):
    """Helper decorator to rewrite a function so that it returns another
    function from it.
    """
    def new_func(*args, **kwargs):
        def processor(stream):
            return f(stream, *args, **kwargs)
        return processor
    return update_wrapper(new_func, f)


def generator(f):
    """Similar to the :func:`processor` but passes through old values
    unchanged and does not pass through the values as parameter.
    """
    @processor
    def new_func(stream, *args, **kwargs):
        for item in stream:
            yield item
        for item in f(*args, **kwargs):
            yield item
    return update_wrapper(new_func, f)


def copy_filename(new, old):
    new.filename = old.filename
    return new


@cli.command('fasta')
@click.option('-f', '--fasta', 'fastas', type=click.Path(), multiple=True, help='The FASTA file to open.')
@generator
def cmd_open_fasta(fastas):
    """Loads one or FASTA files for processing.
    """
    for fasta in fastas:
        try:
            click.echo('Opening "%s"' % fasta)
            file_handle = click.open_file(fasta)
            inf_fasta = FASTA(file_handle)
            yield inf_fasta.read()
        except Exception as e:
            click.echo('Could not open FASTA "%s": %s' % (fasta, e), err=True)


@cli.command('fastq')
@click.option('-q', '--fastq', 'fastqs', type=click.Path(),
              multiple=True, help='The FASTQ file to open.')
@generator
def cmd_open_fastq(fastqs):
    """Loads one or FASTQ files for processing.
    """
    for fastq in fastqs:
        try:
            click.echo('Opening "%s"' % fastq)
            yield FASTQ2(fastq)
        except Exception as e:
            click.echo('Could not open FASTQ "%s": %s' % (fastq, e), err=True)


@cli.command('fastq_to_fasta')
@click.option('--filename', default='%s.fna', type=click.Path(),
              help='The filename.',
              show_default=True)
@processor
def cmd_fastq_to_fasta(fastqs, filename):
    for fastq in fastqs:
        try:
            fn_outf_fastq = filename % '.'.join(os.path.basename(fastq.filename).split('.')[:-1])
            with fastq as fh_fastq:
                with click.open_file(fn_outf_fastq, 'w') as outf:
                    for header, sequence, qualities in fh_fastq:
                        outf.write('>%s\n%s\n' % (header, sequence))
            yield 'Done converting "%s" to FASTA file at "%s"' % (fastq.filename, fn_outf_fastq)
        except Exception as e:
            click.echo('Could not save image "%s": %s' % (fastq.filename, e), err=True)
