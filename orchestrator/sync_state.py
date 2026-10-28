"""Compatibility shim for sync_state."""
import sys
from pathlib import Path

_SCRIPTS_DIR = Path(__file__).resolve().parent.parent / 'scripts'
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

from sync_state import *
if __name__ == '__main__':
    try:
        main()
    except NameError:
        pass
