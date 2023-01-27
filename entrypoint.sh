#!/bin/sh

if [ "$DATABASE" = "mysql" ]
then
    echo "Waiting for mysql..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
      sleep 0.1
    done

    echo "MySQL started"
fi

python manage.py flush --no-input
python manage.py migrate
if ["$INITIAL_DATA" = "True"]
then
  python fake_data_generator.py
fi

exec "$@"
