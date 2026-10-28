"""Compatibility shim for fast_track."""
import sys
from pathlib import Path

_SCRIPTS_DIR = Path(__file__).resolve().parent.parent / 'scripts'
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

from fast_track import *
if __name__ == '__main__':
    try:
        main()
    except NameError:
        pass
