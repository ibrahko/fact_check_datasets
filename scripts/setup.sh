#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/../backend"

python -m pip install --upgrade pip
pip install -r requirements.txt
python manage.py migrate
python manage.py collectstatic --noinput
