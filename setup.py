from setuptools import setup, find_packages

__author__ = "Knights Lab"
__copyright__ = "Copyright (c) 2016--, %s" % __author__
__credits__ = ["Benjamin Hillmann", "Gabe Al-Ghalith", "Tonya Ward", "Pajua Vangay", "Dan Knights"]
__email__ = "hillmannben@gmail.com"
__license__ = "GPL"
__maintainer__ = "Benjamin Hillmann"
__version__ = "0.0.1-dev"

long_description = ''

setup(
    name='ninja_utils',
    version=__version__,
    packages=find_packages(),
    url='',
    license=__license__,
    author=__author__,
    author_email=__email__,
    description='',
    long_description=long_description,
    entry_points={
        'console_scripts': [
            'soft_mask2hard_mask = ninja_utils.scripts.soft_mask2hard_mask:soft_mask2hard_mask',
            'linearize_fasta = ninja_utils.scripts.linearize_fasta:linearize_fasta',
            'timeit = ninja_utils.scripts.timeit:timeit',
            'subset_fasta = ninja_utils.scripts.subset_fasta:subset_fasta',
            'fastq_to_fasta = ninja_utils.scripts.fastq_to_fasta:fastq_to_fasta',
            'filter_dusted_fasta = ninja_utils.scripts.filter_dusted_fasta:filter_dusted_fasta',
        ]
    },
    # scripts=glob(os.path.join('scripts', '*py')),
    keywords='',
    install_requires=['click', 'pyyaml']
)
