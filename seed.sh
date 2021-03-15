#!/bin/bash

rm -rf parktosleepAPI/migrations
rm db.sqlite3
python manage.py migrate
python manage.py makemigrations parktosleepAPI
python manage.py migrate parktosleepAPI
python manage.py loaddata users
python manage.py loaddata tokens
python manage.py loaddata daysoftheweek
python manage.py loaddata rentee
python manage.py loaddata rentalpost
python manage.py loaddata daysavailable
python manage.py loaddata bookedspot 
