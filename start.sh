#!/usr/bin/env bash
until
source venv/bin/activate;
python3 flask run;
 do
    echo "..."
    sleep 1
done
