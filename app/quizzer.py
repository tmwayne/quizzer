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


