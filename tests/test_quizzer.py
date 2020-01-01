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

class Test_QuizDataLoader(unittest.TestCase):

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

    ## TESTS
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

class Test_QuizGenerator(unittest.TestCase):

    ## SETUP
    ##############################
    def setUp(self):
        with open('quiz_valid.csv', 'w') as f_out:
            f_out.writelines(['question,answer\n', 'q1,a1\n', 'q2,a2\n'])
        quiz_data = QuizDataLoader()
        quiz_data.from_csv('quiz_valid.csv')
        self.quiz = QuizGenerator(data=quiz_data)

    def tearDown(self):
        os.remove('quiz_valid.csv')
        del self.quiz

    ## TESTS
    ##############################
    def test_question_generation(self):
        quiz = self.quiz
        quiz.generate_quiz(field=0, shuffle=False)

        quiz.ask_question()
        self.assertEqual(quiz.question, 'q1')

        quiz.ask_question()
        self.assertEqual(quiz.question, 'q2')

        quiz.ask_question()
        self.assertIsNone(quiz.question)

    def test_response_checking(self):
        quiz = self.quiz
        quiz.generate_quiz(field=0, shuffle=False)

        quiz.ask_question()
        self.assertEqual(quiz.question, 'q1')
        quiz.give_response('a1')
        self.assertTrue(quiz.check_response())

        quiz.give_response('a2')
        self.assertFalse(quiz.check_response())

    def test_response_checking_rev(self):
        quiz = self.quiz
        quiz.generate_quiz(field=1, shuffle=False)

        quiz.ask_question()
        self.assertEqual(quiz.question, 'a1')
        quiz.give_response('q1')
        self.assertTrue(quiz.check_response())

        quiz.give_response('q2')
        self.assertFalse(quiz.check_response())

    def test_question_scoring(self):
        quiz = self.quiz
        quiz.generate_quiz(field=0, shuffle=False)

        quiz.ask_question()
        quiz.give_response('a1')
        quiz.update_scores()
        self.assertEqual(quiz.score_quiz(), 1.0)

        quiz.ask_question()
        quiz.give_response('a4') # Give incorrect response
        quiz.update_scores()
        self.assertEqual(quiz.score_quiz(), .5)

    def test_return_misses(self):
        quiz = self.quiz
        quiz.generate_quiz(field=0, shuffle=False)

        quiz.ask_question()
        quiz.give_response('a1')
        quiz.update_scores()
        self.assertEqual(quiz.return_misses(), [])

        quiz.ask_question()
        quiz.give_response('a4') # Give incorrect response
        quiz.update_scores()
        self.assertEqual(quiz.return_misses(), [['q2', 'a2']])

class Test_QuizAdministator(unittest.TestCase):

    ## SETUP
    ##############################
    def setUp(self):
        pass

    def tearDown(self):
        pass


    ## TESTS
    ##############################


######################################################################
### MAIN
######################################################################

if __name__ == '__main__':
    unittest.main()


