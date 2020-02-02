#!env/bin python3
# -*- coding:utf-8  -*-
from controller import log
from app import manager

if __name__ == '__main__':
    log.start()
    manager.run()
