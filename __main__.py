#!/usr/bin/env python3
#! -*- coding: utf-8 -*-

"""
description: Give quiz 
author: Tyler Wayne
data created: 2019-12-31
last modified: 2020-01-01
"""

######################################################################
### SETUP
######################################################################

import json
import logging
import argparse
from logging.config import fileConfig

fileConfig('configs/logging.ini')
logger = logging.getLogger()

from app.quizzer import QuizDataLoader

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

    parser = argparse.ArgumentParser(description='Description')
    parser.add_argument('quiz_file', nargs=1, help='Input file')
    parser.add_argument('-n', nargs=1, help='Number of questions')
    parser.add_argument('--field', nargs=1, help='Field number of question')
    parser.add_argument('--misses_file', nargs=1, help='File to save misses to')
    
    args = parser.parse_args()
    quiz_file = args.quiz_file[0] 
    misses_file = args.misses_file[0] if args.misses_file else '/dev/null/'
    num_questions = args.n[0] if args.n else -1
    question_field = args.field[0] if args.field else 0
    
