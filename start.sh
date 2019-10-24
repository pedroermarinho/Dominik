#!/usr/bin/env bash
until
sudo venv/bin/python3.7 Telegram.py ;
 do
    echo "..."
    sleep 1
done
