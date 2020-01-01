#!/usr/bin/env python3
#! -*- coding: utf-8 -*-

"""
description: Quizzer class
author: Tyler Wayne
data created: 2019-12-31
last modified: 2020-01-01
"""

######################################################################
### SETUP
######################################################################

import csv
import random
import statistics

######################################################################
### FUNCTIONS
######################################################################

class QuizDataLoader():
    def __init__(self):
        self.body = None
        self.header = None

    def _check_data(self, data):
        if len(data) == 0:
            raise MissingQuizData('Input is empty')
        elif len(data) == 1:
            raise MissingQuizBody('Input required to have more than 1 row')
        elif any(len(row) != 2 for row in data):
            raise MalformedQuizData('Input required to have two values per row')
            
    def from_csv(self, file_name):
        with open(file_name, 'r') as f_in:
            csv_reader = csv.reader(f_in, delimiter=',')
            data = [row for row in csv_reader]

            self._check_data(data)
            self.header = data[0]
            self.body = data[1:]

class QuizGenerator():
    ## Public attributes
    question = None
    answer = None
    response = None
    scores = None

    ## Private attributes
    _quiz_header = None
    _quiz_body = None
    _question_field = None
    _answer_field = None
    _question_list = None
    _question_num = None

    def __init__(self, data):
        assert(type(data) == QuizDataLoader)
        self._quiz_header = data.header
        self._quiz_body = data.body

    def generate_quiz(self, field=0, random=False):
        self._question_field = field
        self._answer_field = (field - 1) % 2

        quiz_len = len(self._quiz_body)
        self._question_list = list(range(quiz_len))
        self.scores = [0] * quiz_len

        if random:
            random.shuffle(self._question_list)
        else:
            self._question_list.reverse()

    def ask_question(self):
        if self._question_list:
            self._question_num = self._question_list.pop()
            self.question = self._quiz_body[self._question_num]\
                [self._question_field]
            self.answer = self._quiz_body[self._question_num][self._answer_field]
        else:
            self.question = None
            self.answer = None

    def give_response(self, response):
        self.response = response

    def check_response(self):
        return self.answer == self.response

    def update_scores(self):
        is_correct = self.check_response()
        self.scores[self._question_num] = 1 if is_correct else -1
        
    def score_quiz(self):
        was_asked = lambda x: x != 0
        output = statistics.mean(filter(was_asked, self.scores))
        return (output + 1) / 2

    def return_misses(self):
        return [x[1] for x in zip(self.scores, self._quiz_body) if x[0] == -1]


## EXCEPTIONS
##############################

class MalformedQuizData(Exception):
    pass

class MissingQuizData(Exception):
    pass

class MissingQuizBody(Exception):
    pass

