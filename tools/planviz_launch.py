"""Launch PlanViz sized for one monitor instead of the whole desktop.

WSLg reports all monitors as one X screen (two 2560x1440 monitors -> 5120x1440), and
PlanViz sizes its window from winfo_screenwidth/height, so the window spans every
monitor. This launcher makes Tk report a single-monitor size and puts the main window
on the primary monitor, then runs PlanViz/script/run.py unchanged.

Environment overrides:
  PLANVIZ_SCREEN=WIDTHxHEIGHT  monitor size to fit into (default: Windows primary
                               monitor work area, queried via powershell.exe)
  PLANVIZ_SCALE=0.85           fraction of that size to use for the window
"""
import os
import re
import runpy
import subprocess
import sys
import tkinter
from pathlib import Path

RUN_PY = Path(__file__).resolve().parent.parent / "PlanViz" / "script" / "run.py"


def primary_work_area():
    """(x, y, width, height) of the monitor to fit into, or None if unknown."""
    env = os.environ.get("PLANVIZ_SCREEN")
    if env:
        w, h = (int(v) for v in env.lower().split("x"))
        return 0, 0, w, h
    ps = ("Add-Type -AssemblyName System.Windows.Forms; "
          "$a=[System.Windows.Forms.Screen]::PrimaryScreen.WorkingArea; "
          "\"$($a.X) $($a.Y) $($a.Width) $($a.Height)\"")
    try:
        out = subprocess.run(["powershell.exe", "-NoProfile", "-Command", ps],
                             capture_output=True, text=True, timeout=15).stdout
        x, y, w, h = (int(v) for v in out.split())
        return x, y, w, h
    except Exception:
        return None


def patch_tk(area, scale):
    mx, my, mw, mh = area
    w, h = int(mw * scale), int(mh * scale)
    orig_sw = tkinter.Misc.winfo_screenwidth
    orig_sh = tkinter.Misc.winfo_screenheight
    tkinter.Misc.winfo_screenwidth = lambda self: min(w, orig_sw(self))
    tkinter.Misc.winfo_screenheight = lambda self: min(h, orig_sh(self))

    # PlanViz sets the main window to "WxH" without a position; centre it on the monitor.
    orig_geometry = tkinter.Wm.wm_geometry
    size_only = re.compile(r"^(\d+)x(\d+)$")

    def wm_geometry(self, newGeometry=None):
        if newGeometry and isinstance(self, tkinter.Tk):
            m = size_only.match(str(newGeometry))
            if m:
                gw, gh = min(int(m[1]), w), min(int(m[2]), h)
                newGeometry = f"{gw}x{gh}+{mx + (mw - gw) // 2}+{my + (mh - gh) // 2}"
        return orig_geometry(self, newGeometry)

    tkinter.Wm.wm_geometry = tkinter.Wm.geometry = wm_geometry


def main():
    area = primary_work_area()
    if area:
        patch_tk(area, float(os.environ.get("PLANVIZ_SCALE", "0.85")))
    sys.path.insert(0, str(RUN_PY.parent))
    sys.argv = [str(RUN_PY)] + sys.argv[1:]
    runpy.run_path(str(RUN_PY), run_name="__main__")


if __name__ == "__main__":
    main()
