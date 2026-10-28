import sys
from pathlib import Path
_SCRIPTS_WF = Path(__file__).resolve().parent.parent.parent / 'scripts' / 'workflows'
if str(_SCRIPTS_WF) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_WF))
