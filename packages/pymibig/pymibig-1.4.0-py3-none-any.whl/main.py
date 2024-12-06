"""
The main module of the package.
Responsible for calling other modules' functions.
"""

import sys
import os
from src.pymibig.download_json import download_json
from src.pymibig.download_nucl import download_nucl
from src.pymibig.download_aa import download_aa
from src.pymibig.save_access_codes import save_access_codes
from src.pymibig.save_nucl import save_nucl
from src.pymibig.save_aa import save_aa
from src.pymibig.console import console
from src.pymibig.get_args import get_args

basedir: str = os.path.dirname(__file__)

def main() -> None:
    '''
    Execute functions calls, takes no arguments and has no return.
    '''
    args = get_args()

    download_json(basedir)
    download_nucl(basedir)
    download_aa(basedir)

    access_codes = save_access_codes(args, basedir)
    save_nucl(args, access_codes, basedir)
    save_aa(args, access_codes, basedir)

    console.print(
        '[bold blue]Task completed! Check your result files.[/bold blue]'
        )

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit('\nExecution interrupted by the user.')
