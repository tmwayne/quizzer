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
    question = None
    answer = None
    response = None

    def __init__(self, data):
        assert(type(data) == QuizDataLoader)
        self._quiz_header = data.header
        self._quiz_body = data.body

    def generate_quiz(self, field=0, random=False):
        self._question_field = field
        self._answer_field = (field - 1) % 2

        quiz_len = len(self._quiz_body)
        self._question_list = list(range(quiz_len))

        if random:
            random.shuffle(self._question_list)
        else:
            self._question_list.reverse()

    def ask_question(self):
        if self._question_list:
            question = self._question_list.pop()
            self.question = self._quiz_body[question][self._question_field]
            self.answer = self._quiz_body[question][self._answer_field]
        else:
            self.question = None
            self.answer = None

    def give_response(self, response):
        self.response = response

    def check_response(self):
        return self.answer == self.response


## EXCEPTIONS
##############################

class MalformedQuizData(Exception):
    pass

class MissingQuizData(Exception):
    pass

class MissingQuizBody(Exception):
    pass


######################################################################
### CONFIGURATIONS
######################################################################

configs = {
}


