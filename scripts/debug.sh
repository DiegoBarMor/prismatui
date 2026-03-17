#!/bin/bash
set -eu

./scripts/reinstall.sh
clear

mkdir -p logs
python3 examples/00_keys.py
python3 examples/01_colors.py
python3 examples/02_images.py
python3 examples/03_layouts.py
python3 examples/04_movement.py
rm -rf logs
