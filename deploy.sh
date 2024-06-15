#!/bin/sh
cd /var/www/buildblog
source /var/www/.venv/bin/activate
git pull origin master
pip3 install -r requirements.txt
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py collectstatic --noinput
sudo systemctl restart apache2
