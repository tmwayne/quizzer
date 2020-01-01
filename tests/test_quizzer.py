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

######################################################################
### FUNCTIONS
######################################################################

class TestCase(unittest.TestCase):

    quizzes = {
        'quiz_valid.csv': ['question,answer\n', 'q1,a1\n', 'q2,a2\n'],
        'quiz_missing_answer.csv': ['question,answer\n', 'q1\n', 'q2,a2\n'],
        'quiz_extra_comma.csv': ['question,answer\n', 'q1,,a1\n', 'q2,a2\n'],
        'quiz_no_questions.csv': ['question,answer\n'],
        'quiz_empty.csv': [],
    }

    ## SETUP
    ##############################

    def setUp(self):
        """ Write quiz files for different cases """
        for file_name, quiz in self.quizzes.items():
            with open(file_name, 'w') as f_out:
                f_out.writelines(quiz)

    def tearDown(self):
        """ Remove quiz files from disk """
        for file_name in self.quizzes.keys():
            os.remove(file_name)

    def test_load_valid_quiz(self):
        pass

    def test_load_malformed_quiz(self):
        pass



######################################################################
### MAIN
######################################################################

if __name__ == '__main__':
    unittest.main()


