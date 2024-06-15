#!/usr/bin/env bash
ssh -o StrictHostKeyChecking=no ubuntu@buildblog.in << 'ENDSSH'
 cd /var/www/buildblog
 source /var/www/.venv/bin/activate
 sudo service apache2 stop
 git pull origin master
 pip install -r requirements.txt
 python3 manage.py makemigrations
 python3 manage.py migrate
 python3 manage.py collectstatic --noinput
 sudo service apache2 restart
ENDSSH