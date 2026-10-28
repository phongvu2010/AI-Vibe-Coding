"""
Orchestrator package compatibility layer for AI-Vibe-Coding.
Exposes core SDLC orchestrator components while routing to scripts.* internally.
"""
import sys
from pathlib import Path

__version__ = "2.0.0"

_SCRIPTS_DIR = Path(__file__).resolve().parent.parent / 'scripts'
if str(_SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(_SCRIPTS_DIR))

# Convenient direct package-level exports
try:
    from runner import SDLCOrchestrator, main as run_sdlc
    from agent_factory import AgentFactory, ModelRouter
    from fast_track import FastTrackOrchestrator, analyze_task_impact
    from sync_state import VibeStateSynchronizer
    from state import SDLCState, SDLCPhase, GateDecision, GateDecisionStatus
    from release_bundler import ReleaseBundler
    from persistence import StatePersistence
    from synthesis_engine import AdaptiveCodeSynthesizer

    __all__ = [
        "__version__",
        "SDLCOrchestrator",
        "run_sdlc",
        "AgentFactory",
        "ModelRouter",
        "FastTrackOrchestrator",
        "analyze_task_impact",
        "VibeStateSynchronizer",
        "SDLCState",
        "SDLCPhase",
        "GateDecision",
        "GateDecisionStatus",
        "ReleaseBundler",
        "StatePersistence",
        "AdaptiveCodeSynthesizer",
    ]
except Exception as e:
    # If dependencies are missing in the current python env, skip export gracefully
    pass

