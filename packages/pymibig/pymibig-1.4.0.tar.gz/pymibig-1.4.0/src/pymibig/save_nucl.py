"""
Save the matched nucleotide sequences in FASTa format.
"""

import sys
import tarfile
import io
from itertools import islice
from rich.progress import track
from Bio import SeqIO
from src.pymibig.console import console
from src.pymibig.constants import NUCLEOTIDE

def save_nucl(args, access_codes: str, basedir: str) -> None:
    '''
    Save the desired nucleotide sequences in a FASTa file.

    Arguments:
    args -- object of class Args containing user inputs
    access_codes -- codes list to retrieve from database
    basedir -- main module path
    '''
    desired_seqs: list = []

    try:
        with tarfile.open(f'{basedir}/src/db/{NUCLEOTIDE}') as tar:
            for member in track(islice(tar, 1, None),
            description='[bold green]Saving nucleotide '
                        'sequences...[/bold green]',
            total=len(tar.getmembers())-1):
                with tar.extractfile(member) as handle:
                    seq = SeqIO.read(
                        io.TextIOWrapper(handle),
                        'genbank')
                    if any(code in seq.id for code in access_codes):
                        desired_seqs.append(seq)

        SeqIO.write(
            desired_seqs,
            f'{args.create_prefix}_nucl.fasta', 'fasta')
    except PermissionError:
        console.print(
            '[bold red]Permission to read directory or write file '
            'denied.[/bold red]'
            )
        sys.exit()
