#!/usr/bin/env python3
#! -*- coding: utf-8 -*-

"""
description: Give quiz 
author: Tyler Wayne
data created: 2019-12-31
last modified: 2019-12-31
"""

######################################################################
### SETUP
######################################################################

import json
import logging
from logging.config import fileConfig

fileConfig('configs/logging.ini')
logger = logging.getLogger()


######################################################################
### FUNCTIONS
######################################################################


######################################################################
### CONFIGURATIONS
######################################################################

try:
    with open('configs/configs.json', 'r') as f:
        configs = json.load(f)
except Exception as e:
    logger.exception('Unable to load configuration file')

######################################################################
### MAIN
######################################################################

if __name__ == '__main__':

