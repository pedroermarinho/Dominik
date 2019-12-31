#!/usr/bin/env bash
until
source venv/bin/activate;
python3 run.py runserver;
 do
    echo "..."
    sleep 1
done
