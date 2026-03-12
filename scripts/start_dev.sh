#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/../backend"
python manage.py runserver 0.0.0.0:8000
