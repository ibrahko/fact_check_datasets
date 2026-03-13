#!/usr/bin/env bash
set -euo pipefail

STATIC_ROOT="${STATIC_ROOT:-/app/staticfiles}"
export STATIC_ROOT

mkdir -p "${STATIC_ROOT}"
python manage.py collectstatic --noinput --clear -v 2
python manage.py migrate --noinput
python manage.py showmigrations --plan
python manage.py shell -c "from django.db import connections; connections['default'].cursor(); print('Database connection OK')"

if [ -n "${DJANGO_SUPERUSER_EMAIL:-}" ]; then
  echo "import os; from django.contrib.auth import get_user_model; U=get_user_model(); email=os.environ.get('DJANGO_SUPERUSER_EMAIL',''); username=os.environ.get('DJANGO_SUPERUSER_USERNAME', email or 'admin'); password=os.environ.get('DJANGO_SUPERUSER_PASSWORD','admin123'); email and (U.objects.filter(email=email).exists() or U.objects.create_superuser(username=username, email=email, password=password))" | python manage.py shell
fi
