# -*- coding: utf-8 -*-

"""
Tests for core
"""
import unittest
from mock_sepyresults import QUESTION
from mock_sepyresults import QUESTIONS
from mock_sepyresults import ANSWER
from mock_sepyresults import EMPTY_QUESTIONS
from mock_sepyresults import EMPTY_ANSWERS
from app.core.stackprinterdownloader import StackExchangeDownloader
from django.utils import simplejson 

class StackprinterDownloaderTestCase(unittest.TestCase):
    
    def setUp(self):
        self.spdownloader = StackExchangeDownloader('stackoverflow') 
        self.spdownloader.retriever = MockRetriever()
    def test_get_question(self):     
        assert self.spdownloader.get_question(9) is not None
    def test_get_question(self):     
        assert self.spdownloader.get_question(0) is None
    def test_get_question_title(self):     
        assert self.spdownloader.get_question_title(9)== "How do I calculate someone's age in C#?"        
    def test_get_answer_quicklook(self):
        assert self.spdownloader.get_answer_quicklook(22) is not None
    def test_get_answer_quicklook(self):
        assert self.spdownloader.get_answer_quicklook(0) is None
    def test_get_questions_by_tags(self):
        assert len(self.spdownloader.get_questions_by_tags('cooltags', 1)[0]) > 50
    def test_get_questions_by_tags(self):
        assert len(self.spdownloader.get_questions_by_tags('suckstags', 1)[0]) == 0 
    def test_get_questions_by_votes(self):
        assert len(self.spdownloader.get_questions_by_votes(1)[0]) > 0
    def test_get_answers(self):  
        pass

    def test_get_users_by_id(self):   
        pass

    def test_get_users(self):    
        pass

    def test_get_favorites_questions(self): 
        pass

    def test_get_tags(self):
        pass

class MockRetriever():
    def get_question(self, question, api_endpoint, **kwargs):
        if question == 9:
            return simplejson.loads(QUESTION)
        if question == 0:
            return simplejson.loads(EMPTY_QUESTIONS)    
    def get_answer(self, answer, api_endpoint, **kwargs):
        if answer == 22:
            return simplejson.loads(ANSWER)
        if answer == 0:
            return simplejson.loads(EMPTY_ANSWERS)
    def get_questions_by_tags(self, tags, api_endpoint, page, **kwargs):
        if tags == 'cooltags':
            return simplejson.loads(QUESTIONS)
        if tags == 'suckstags':
            return simplejson.loads(EMPTY_QUESTIONS)
    def get_questions(self, api_endpoint, page, **kwargs):
        return simplejson.loads(QUESTIONS)

if __name__ == '__main__':
    unittest.main()
