#!/usr/bin/env bash
# exit on error
set -o errexit

#poetry install
pip install --upgrade pip #Update pip version
pip --version # Check pip version
pip install -r requirements.txt # Install dependencies using requirements.txt

python3 manage.py collectstatic --no-input # Collect all necesary static files
python3 manage.py migrate # Migrate changes to DB
