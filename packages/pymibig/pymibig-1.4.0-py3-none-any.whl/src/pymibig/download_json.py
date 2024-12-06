"""
Download JSON metadta files from MIBiG
"""

import os
import sys
import requests
from rich.progress import track
from src.pymibig.console import console
from src.pymibig.constants import JSON_LINK, METADATA, CHUNK_SIZE

def download_json(basedir: str) -> None:
    '''
    Download JSON files tar.gz compressed.

    Argumnents:
    basedir -- main module path
    '''
    if not os.path.exists(f'{basedir}/src/db/{METADATA}'):
        try:
            resp = requests.get(JSON_LINK, stream=True, timeout=60)
            total_size = int(resp.headers.get('content-length', 0))
            with open(f'{basedir}/src/db/{METADATA}', mode='wb') as file:
                for chunk in track(resp.iter_content(chunk_size=CHUNK_SIZE),
                description='[bold green]Downloading MIBiG metadata'
                            '...[/bold green]',
                total=total_size / CHUNK_SIZE):
                    file.write(chunk)
        except PermissionError:
            console.print('[bold red]File can not be writen.[/bold red]')
            sys.exit()
        except requests.exceptions.RequestException:
            console.print('[bold red]Connection error or timed '
                          'out.[/bold red]')
    else:
        console.print('[bold green]Loading JSON metadata...[/bold green]')
