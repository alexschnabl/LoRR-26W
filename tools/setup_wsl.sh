#!/usr/bin/env bash
# One-time setup of the Ubuntu 24.04 WSL distro for the LoRR Start-Kit
# (ATAI WS26, Assignment 1). Safe to re-run.
#
# Run from Windows as root (from the repository root):
#   wsl -d Ubuntu-24.04 -u root -- bash tools/setup_wsl.sh
set -euo pipefail

PROJECT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PYBIND11_VERSION=3.0.1   # Start-Kit needs pybind11 >= 3.0.1; Ubuntu 24.04 only ships 2.11

export DEBIAN_FRONTEND=noninteractive
apt-get update
apt-get install -y \
  build-essential cmake git \
  libboost-program-options-dev libboost-system-dev libboost-filesystem-dev libboost-log-dev \
  python3-dev python3-pip python3-venv python3-tk \
  python3-numpy python3-scipy python3-matplotlib python3-pandas python3-pil python3-pil.imagetk

# pybind11: install the CMake package + headers into /usr/local so find_package(pybind11) picks it up.
if ! grep -qs "PYBIND11_VERSION_MAJOR 3" /usr/local/include/pybind11/detail/common.h; then
  tmp=$(mktemp -d)
  git clone --depth 1 --branch "v${PYBIND11_VERSION}" https://github.com/pybind/pybind11.git "$tmp/pybind11"
  cmake -S "$tmp/pybind11" -B "$tmp/build" -DPYBIND11_TEST=OFF
  cmake --install "$tmp/build"
  rm -rf "$tmp"
fi

# PlanViz: own venv with its pinned requirements (numba is not in apt); tkinter comes from python3-tk.
if [ -f "$PROJECT/PlanViz/requirements.txt" ]; then
  [ -x /opt/planviz-venv/bin/python ] || python3 -m venv /opt/planviz-venv
  /opt/planviz-venv/bin/pip install -q --upgrade pip
  /opt/planviz-venv/bin/pip install -q -r "$PROJECT/PlanViz/requirements.txt"
  cat > /usr/local/bin/planviz <<EOF
#!/usr/bin/env bash
# Usage: planviz --map <file.map> --plan <output.json> [PlanViz options]
# tools/planviz_launch.py keeps the window on one monitor (WSLg reports all monitors as one screen).
exec /opt/planviz-venv/bin/python "$PROJECT/tools/planviz_launch.py" "\$@"
EOF
  chmod +x /usr/local/bin/planviz
fi

echo
echo "== versions"
cmake --version | head -1
g++ --version | head -1
python3 --version
grep -E "define PYBIND11_VERSION_(MAJOR|MINOR|PATCH)" /usr/local/include/pybind11/detail/common.h
dpkg -s libboost-log-dev | grep '^Version'
