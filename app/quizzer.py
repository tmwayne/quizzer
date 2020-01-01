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

    @staticmethod
    def _check_data(data):
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

    def __init__(self, data):
        assert(type(data) == QuizDataLoader)
        self.question = None
        self.answer = None
        self.response = None
        self.scores = None

        self._quiz_header = data.header
        self._quiz_body = data.body
        self._question_field = None
        self._answer_field = None
        self._question_list = None
        self._question_num = None
        self._misses_file = None

    def generate_quiz(self, num=0, field=0, misses_file=None, shuffle=False):
        self._question_field = field % 2
        self._answer_field = (field - 1) % 2
        self._misses_file = misses_file

        quiz_len = len(self._quiz_body)
        question_list = list(range(quiz_len))
        self.scores = [0] * quiz_len

        if shuffle:
            random.shuffle(question_list)
        else:
            question_list.reverse()

        if num < 1 or num > quiz_len:
            self._question_list = question_list
        else:
            self._question_list = question_list[-1*num:]


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

    def write_misses(self):
        misses = self.return_misses()
        if self._misses_file and misses:
            with open(self._misses_file, 'w') as f_out:
                csv_writer = csv.writer(f_out, delimiter=',')
                csv_writer.writerow(self._quiz_header)
                for row in misses:
                    csv_writer.writerow(row)
            

class QuizAdministrator():

    def __init__(self, data, num, field, misses_file):
        self.quiz_data = data
        self.num = num
        self.field = field
        self.misses_file = misses_file
        self.score = None

    def start_quiz(self):
        quiz = QuizGenerator(data=self.quiz_data)
        quiz.generate_quiz(
            num=self.num, 
            field=self.field,
            misses_file=self.misses_file,
            shuffle=True
        )
        quiz.ask_question()
        while quiz.question:
            response = input("%s: " % quiz.question)
            quiz.give_response(response)
            quiz.check_response()
            quiz.update_scores()
            quiz.ask_question()

        quiz.write_misses()
        print(self._score_quiz(quiz))

    @staticmethod
    def _score_quiz(quiz):
        score = quiz.score_quiz()
        if score > 0.9:
            out = f"Way to go, you scored {score}!"
        elif score > .75:
            out = f"You scored {score}. You're getting there!"
        else:
            out = f"You scored {score}. Keep working at it!"
        return out
        

## EXCEPTIONS
##############################

class MalformedQuizData(Exception):
    pass

class MissingQuizData(Exception):
    pass

class MissingQuizBody(Exception):
    pass

