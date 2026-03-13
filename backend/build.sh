#!/usr/bin/env bash
set -euo pipefail

mkdir -p staticfiles
python manage.py collectstatic --noinput
python manage.py migrate --noinput

if [ -n "${DJANGO_SUPERUSER_EMAIL:-}" ]; then
  echo "import os; from django.contrib.auth import get_user_model; U=get_user_model(); email=os.environ.get('DJANGO_SUPERUSER_EMAIL',''); username=os.environ.get('DJANGO_SUPERUSER_USERNAME', email or 'admin'); password=os.environ.get('DJANGO_SUPERUSER_PASSWORD','admin123'); email and (U.objects.filter(email=email).exists() or U.objects.create_superuser(username=username, email=email, password=password))" | python manage.py shell
fi
