#!/bin/bash
set -eu

python3 -m build
twine upload dist/*
rm -rf build dist prismatui.egg-info
