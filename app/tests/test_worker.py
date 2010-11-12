# -*- coding: utf-8 -*-

"""
Tests for utility
"""

import unittest
from app.utility.worker import deferred_store_question_to_cache, deferred_store_answers_to_cache
import app.db.question as dbquestion
from app.core.stackprinterdownloader import StackExchangeDownloader

class WorkerTestCase(unittest.TestCase):
    def setUp(self):
        self.spdownloader = StackExchangeDownloader('stackoverflow')
    def test_answers_save_and_get_from_datastore(self):
        answers = ['dict1', 'dict2', 'dict3', 'dict4']
        question_id = 1
        service = 'foo'
        deferred_store_answers_to_cache(question_id, service, answers)
        answers_from_cache = dbquestion.get_answers(question_id, service)
        self.assertEquals(answers, answers_from_cache)
        
        #636 answers
        answers = self.spdownloader.get_answers(58640)
        deferred_store_answers_to_cache(58640, 'stackoverflow', answers)
        answers_from_cache = dbquestion.get_answers(58640, 'stackoverflow')
        self.assertEquals(answers, answers_from_cache)
        
        #148 answers
        answers = self.spdownloader.get_answers(101268)
        deferred_store_answers_to_cache(101268, 'stackoverflow', answers)
        answers_from_cache = dbquestion.get_answers(101268, 'stackoverflow')
        self.assertEquals(answers, answers_from_cache)
        
        #0 answers
        answers = self.spdownloader.get_answers(3940165)
        deferred_store_answers_to_cache(3940165, 'stackoverflow', answers)
        answers_from_cache = dbquestion.get_answers(3940165, 'stackoverflow')
        self.assertEquals(answers, answers_from_cache)
    def test_question_save_and_get_from_datastore(self):
        question = ['dict1']
        question_id = 1
        service = 'foo'
        deferred_store_question_to_cache(question_id, service, question)
        question_from_cache = dbquestion.get_question(question_id, service)
        self.assertEquals(question, question_from_cache)

        question = self.spdownloader.question(3940165)
        deferred_store_question_to_cache(3940165, 'stackoverflow', answers)
        question_from_cache = dbquestion.get_answers(3940165, 'stackoverflow')
        self.assertEquals(question, question_from_cache)
       
if __name__ == '__main__':
    unittest.main()
