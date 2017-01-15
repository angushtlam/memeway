#!/usr/bin/env bash

source venv/bin/activate

python manage.py runserver &

python chat_bot.py