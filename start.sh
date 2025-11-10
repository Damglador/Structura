#!/bin/sh

set -e
cd "$(dirname "$0")"

if [ ! -d .venv ]; then
	python3 -m venv .venv
	source .venv/bin/activate
	pip3 install -r requirements.txt
else
	source .venv/bin/activate
fi
python3 structura.py
