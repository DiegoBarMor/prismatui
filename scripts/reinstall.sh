#!/bin/bash
set -eu

pip uninstall prismatui -y || true
pip install .
rm -rf build prismatui.egg-info
