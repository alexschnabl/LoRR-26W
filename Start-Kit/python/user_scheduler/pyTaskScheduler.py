"""
pyTaskScheduler.py — loader for our schedulers.

The simulator always imports class pyTaskScheduler from this file. Our schedulers live
outside the Start-Kit (assignment1/ex1/); this file loads the one named by the
environment variable LORR_SCHEDULER (a .py path, absolute or relative to the repository
root) and exposes its pyTaskScheduler class. Default: the naive baseline.
"""
import importlib.util
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
path = Path(os.environ.get("LORR_SCHEDULER") or "assignment1/ex1/naive.py")
if not path.is_absolute():
    path = ROOT / path

sys.path.insert(0, str(path.parent))  # lets the scheduler import helpers next to it
spec = importlib.util.spec_from_file_location("lorr_user_scheduler", path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
print(f"[scheduler] {path.relative_to(ROOT) if path.is_relative_to(ROOT) else path}", file=sys.stderr)

pyTaskScheduler = module.pyTaskScheduler
