"""
Get arguments from user.
"""

import argparse
from src.pymibig.args_class import Args


def get_args() -> Args:
    '''
    Recieve user arguments and return them to main function.
    '''
    parser = argparse.ArgumentParser(
        prog='pyMIBiG',
        description='A small tool to download, match and save targeted '
                    'sequences from MIBiG.'
    )
    parser.add_argument('-o', '--organism',
                        help='Organism name to query in database.',
                        type=str)
    parser.add_argument('-p', '--product', help='Compound to query in database.',
                        type=str)
    parser.add_argument('-b', '--biosynt',
                        help='Biosynthetic class to query in database.',
                        type=str)
    parser.add_argument('-c', '--completeness', help='Loci completeness.',
        type=str, choices=['complete', 'incomplete', 'unknown', 'all'],
        default='all')
    parser.add_argument('-q', '--quality', help='Entry quality level.',
        type=str, choices=['low', 'medium', 'high', 'questionable', 'all'],
        default='all')

    args = parser.parse_args()

    if not (args.organism or args.product or args.biosynt):
        parser.error('At least one of the following arguments is requires: '
                     'organism, product, biosynt')

    return Args(args)
