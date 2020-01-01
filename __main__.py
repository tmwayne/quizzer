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

from app.quizzer import QuizDataLoader, QuizAdministrator

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

    ## PARSE COMMAND-LINE ARGS
    ##############################
    parser = argparse.ArgumentParser(description='Description')
    parser.add_argument('quiz_file', nargs=1, help='Input file')
    parser.add_argument('-n', nargs=1, help='Number of questions')
    parser.add_argument('--field', nargs=1, help='Field number of question')
    parser.add_argument('--misses_file', nargs=1, help='File to save misses to')
    
    args = parser.parse_args()
    quiz_file = args.quiz_file[0] 
    misses_file = args.misses_file[0] if args.misses_file else '/dev/null/'
    num_questions = int(args.n[0]) if args.n else 0
    question_field = int(args.field[0]) if args.field else 0
    
    ## ADMINISTER QUIZ
    ##############################
    quiz_data = QuizDataLoader()
    quiz_data.from_csv(quiz_file)

    quiz = QuizAdministrator(
        data=quiz_data,
        num=num_questions,
        field=question_field,
        misses_file=misses_file
    )

    quiz.start_quiz()
