#!/usr/bin/env python3
#! -*- coding: utf-8 -*-
"""
@description: Program for quizzing capitals
@author: Wayne Tyler
@date_created: 2018-10-23
"""

############################################################
## SET-UP
############################################################

import os
import argparse
import csv
import random
import itertools
from datetime import datetime as dt
from math import floor


############################################################
## FUNCTIONS
############################################################

not_empty = lambda x: len(x) > 0

def calc_test_time(start, stop):

    test_time = (stop - start).total_seconds()
    test_min = int(floor(test_time / 60))
    test_sec = int(test_time % 60)

    return test_min, test_sec

def load_quiz(file, field):
    """Load the quiz from a file"""
    
    ## This selects whether we are prompted capitals or countries
    if field == 0 or field == 1:
        question_ind = field
    else:
        question_ind = random.randint(0, 1)
    
    answer_ind = abs(1 - question_ind)
    
    with open(file, 'r', encoding='utf-8') as f:
        
        reader = csv.reader(f, delimiter=configs['delim'])       
        header = next(reader)
    
        question_val = header[question_ind]
        answer_val = header[answer_ind]
    
        quiz = {
            line[question_ind]: line[answer_ind]
            for line in reader
        }
        
    return quiz, header, question_val, answer_val

def give_quiz(quiz, num, question_val, answer_val):
    """Shuffle the quiz then give it"""
    keys = list(quiz.keys())
    random.shuffle(keys) # Note that this shuffles in place
    
    if num:
        keys = keys[:int(num)]
    
    ## Put all of the misses into this dictionary
    misses = dict()

    start_time = dt.now()
    
    num_missed = 0

    print('Enter the %s for the given %s' % (answer_val, question_val))
    for ind, question in enumerate(keys):
        
        answer = quiz[question].lower().strip()
        guess = ''
        miss = 0
        
        while True:
            ## Prompt the country/capital
            guess = input(str(ind + 1) + '. ' + question + ' : ').lower()

            if guess == answer:
                break
            else:
                miss = 1
            
            ## If no answer is given
            ## then the answer is printed to the console
            ## And the combination is saved
            ## to the misses dictionary
            if guess == '':
                print('%s : %s' % (question, answer))
                misses[question] = answer
                break

        num_missed = num_missed + miss
            
    stop_time = dt.now()
    test_min, test_sec = calc_test_time(start_time, stop_time)

    score = round(100 * (1 - num_missed / (ind + 1)))
    print('You scored %d%% in %s min and %s seconds!'
        % (score, str(test_min), str(test_sec)))

    return misses
   
def save_misses(misses, misses_file, quiz_header):
    """Save the misses to a file"""
    with open(misses_file, 'w', newline='', encoding='utf-8') as f:
        
        writer = csv.writer(f, delimiter=configs['delim'])
        writer.writerow(header[0:2])
        for q, a in misses.items():
            writer.writerow([q, a])

############################################################
## CONFIGURATIONS
############################################################

configs = {
    'delim': '|',
    'encoding': 'utf-8',
}

######################################################################
### MAIN        
######################################################################
                
if __name__ == "__main__":
    
    ## Set up arg parser
    parser = argparse.ArgumentParser(description='Quiz capitals and countries')
    parser.add_argument('file', nargs=1, help='Location of quiz file')
    parser.add_argument(
        '-f', nargs=1, default=[-1], help='Field number for questions'
    )
    parser.add_argument(
        '-m', nargs='?', const='_default', default='', 
        help='Location of file to save misses to'
    )
    parser.add_argument(
        '-n', nargs=1, default=[False], help='Number of questions for quiz'
    )
    
    args = parser.parse_args()
    
    FILE = args.file[0]
    FIELD = int(args.f[0])
    NUM = args.n[0]
    
    file_name, ext = os.path.splitext(os.path.basename(FILE))
    MISSES_FILE = '%s.misses' % file_name if args.m == '_default' else args.m
    
    quiz, header, question_val, answer_val = load_quiz(FILE, FIELD)
    misses = give_quiz(quiz, NUM, question_val, answer_val)
    
    if not_empty(misses) & not_empty(MISSES_FILE):
        save_misses(misses, MISSES_FILE, header)
    

