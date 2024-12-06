"""
Save the matched amino acid sequences in FASTa format.
"""

import sys
import gzip
from rich.progress import track
from Bio import SeqIO
from src.pymibig.console import console
from src.pymibig.constants import AA

def save_aa(args, access_codes: str, basedir: str) -> None:
    '''
    Save the desired amino acid sequences in a FASTa file.

    Arguments:
    args -- object of class Args containing user inputs
    basedir -- main module path
    '''
    desired_seqs: list = []

    try:
        with gzip.open(f'{basedir}/src/db/{AA}', mode='rt') as gz:
            total = len(list(SeqIO.parse(gz, 'fasta')))

        with gzip.open(f'{basedir}/src/db/{AA}', mode='rt') as gz:
            for seq in track(SeqIO.parse(gz, 'fasta'),
            description='[bold green]Saving amino acid '
                        'sequences...[/bold green]',
            total=total):
                if any(code in seq.id for code in access_codes):
                    desired_seqs.append(seq)

        SeqIO.write(
            desired_seqs,
            f'{args.create_prefix}_aa.fasta', 'fasta')
    except PermissionError:
        console.print(
            '[bold red]Permission to read directory or write file '
            'denied.[/bold red]'
            )
        sys.exit()
