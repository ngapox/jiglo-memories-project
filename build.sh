#!/usr/bin/env bash
# exit on error
set -o errexit

export SECRET_KEY=${SECRET_KEY:-'django-insecure-)kaed75@0r17o4c3vh(ok40lnfl)7b^#&djz_-p!kia$f!ratf'}

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate