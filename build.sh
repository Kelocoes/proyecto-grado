#!/usr/bin/env bash
# exit on error
set -o errexit

#poetry install
pip install --upgrade pip
pip install --version
pip install -r requirements.txt

python3 manage.py collectstatic --no-input
python3 manage.py migrate
