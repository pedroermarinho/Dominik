#!/usr/bin/env bash
until
sudo venv/bin/python3.7 telegram.py ;
 do
    echo "..."
    sleep 1
done
