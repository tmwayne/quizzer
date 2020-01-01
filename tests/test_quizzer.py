#!/usr/bin/env python3
#! -*- coding: utf-8 -*-

"""
description: Template for setting up unit tests
author: Tyler Wayne
last modified: 2020-01-01
"""

######################################################################
### SETUP
######################################################################

import unittest
import os

from app.quizzer import (
    QuizDataLoader,
    QuizGenerator,
    MalformedQuizData,
    MissingQuizData,
    MissingQuizBody,
)

######################################################################
### FUNCTIONS
######################################################################

class TestCase(unittest.TestCase):

    ## SETUP
    ##############################
    quizzes = {
        'quiz_valid.csv': ['question,answer\n', 'q1,a1\n', 'q2,a2\n'],
        'quiz_missing_answer.csv': ['question,answer\n', 'q1\n', 'q2,a2\n'],
        'quiz_extra_comma.csv': ['question,answer\n', 'q1,,a1\n', 'q2,a2\n'],
        'quiz_missing_body.csv': ['question,answer\n'],
        'quiz_missing_data.csv': [],
    }

    def setUp(self):
        """ Write quiz files for different cases """
        for file_name, quiz in self.quizzes.items():
            with open(file_name, 'w') as f_out:
                f_out.writelines(quiz)

    def tearDown(self):
        """ Remove quiz files from disk """
        for file_name in self.quizzes.keys():
            os.remove(file_name)

    ## QuizDataLoader
    ##############################
    def test_load_valid_quiz(self):
        quiz_data = QuizDataLoader()
        quiz_data.from_csv('quiz_valid.csv')
        self.assertEqual(quiz_data.header, ['question', 'answer'])
        self.assertEqual(len(quiz_data.body), 2)

    def test_load_malformed_quiz(self):
        try:
            QuizDataLoader().from_csv('quiz_missing_answer.csv')
        except Exception as e:
            self.assertEqual(type(e), MalformedQuizData)

        try:
            QuizDataLoader().from_csv('quiz_extra_comma.csv')
        except Exception as e:
            self.assertEqual(type(e), MalformedQuizData)

        try:
            QuizDataLoader().from_csv('quiz_missing_body.csv')
        except Exception as e:
            self.assertEqual(type(e), MissingQuizBody)

        try:
            QuizDataLoader().from_csv('quiz_missing_data.csv')
        except Exception as e:
            self.assertEqual(type(e), MissingQuizData)

    ## QuizGenerator
    ##############################
    def test_question_generation(self):
        quiz_data = QuizDataLoader()
        quiz_data.from_csv('quiz_valid.csv')
        quiz = QuizGenerator(data=quiz_data)
        quiz.generate_quiz(field=0, random=False)

        quiz.ask_question()
        self.assertEqual(quiz.question, 'q1')

        quiz.ask_question()
        self.assertEqual(quiz.question, 'q2')

        quiz.ask_question()
        self.assertIsNone(quiz.question)

    def test_answer_checking(self):
        quiz_data = QuizDataLoader()
        quiz_data.from_csv('quiz_valid.csv')
        quiz = QuizGenerator(data=quiz_data)
        quiz.generate_quiz()

        quiz.ask_question()
        self.assertEqual(quiz.question, 'q1')
        quiz.give_response('a1')
        self.assertTrue(quiz.check_response())

        quiz.give_response('a2')
        self.assertFalse(quiz.check_response())


######################################################################
### MAIN
######################################################################

if __name__ == '__main__':
    unittest.main()


