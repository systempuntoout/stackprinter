# -*- coding: utf-8 -*-

"""
Tests for core
"""
import unittest
from mock_sepyresults import QUESTION, QUESTIONS, EMPTY_QUESTIONS
from mock_sepyresults import ANSWER, ANSWERS, EMPTY_ANSWERS
from mock_sepyresults import USERS, TAGS
from app.core.stackprinterdownloader import StackExchangeDownloader
from django.utils import simplejson 

class StackprinterDownloaderTestCase(unittest.TestCase):
    
    def setUp(self):
        self.spdownloader = StackExchangeDownloader('stackoverflow') 
        self.spdownloader.retriever = MockRetriever() #Comment to test ONLINE
        
    def test_get_question(self):     
        assert self.spdownloader.get_question(9) is not None
        assert self.spdownloader.get_question(0) is None
        assert self.spdownloader.get_question(9)['creation_date'] == 1217547659
        assert self.spdownloader.get_question(9)['title'] == "How do I calculate someone's age in C#?"
  
    def test_get_question_title(self):     
        assert self.spdownloader.get_question_title(9)== "How do I calculate someone's age in C#?"  
        assert self.spdownloader.get_question_title(0) is None       
        
    def test_get_answer_quicklook(self):
        assert self.spdownloader.get_answer_quicklook(22) is not None
        assert self.spdownloader.get_answer_quicklook(22)['title'] != ''
        assert self.spdownloader.get_answer_quicklook(0) is None
                
    def test_get_questions_by_tags(self):
        assert len(self.spdownloader.get_questions_by_tags('python', 1)[0]) > 0
        assert self.spdownloader.get_questions_by_tags('python', 1)[1].total > 0
        assert len(self.spdownloader.get_questions_by_tags('atagthedoesnotexist', 1)[0]) == 0 
        assert self.spdownloader.get_questions_by_tags('atagthedoesnotexist', 1)[1].total == 0
        assert self.spdownloader.get_questions_by_tags('python', 1)[0][0].question_id > 0
        assert self.spdownloader.get_questions_by_tags('python', 1)[0][0].url.startswith('http')
        assert self.spdownloader.get_questions_by_tags('python', 1)[0][0].service != ''

    def test_get_questions_by_votes(self):
        assert len(self.spdownloader.get_questions_by_votes(page = 1)[0]) > 0
        assert self.spdownloader.get_questions_by_votes(page = 1)[1].total > 0
        assert self.spdownloader.get_questions_by_votes(page = 1)[0][0].question_id > 0
        assert self.spdownloader.get_questions_by_votes(page = 1)[0][0].url.startswith('http')
        assert self.spdownloader.get_questions_by_votes(page = 1)[0][0].service != ''

    def test_get_answers(self):
        assert len(self.spdownloader.get_answers(656155)) == 3
        assert self.spdownloader.get_answers(656155)[0]['title'] != ''
        assert len(self.spdownloader.get_answers(9033)) == 303
        assert len(self.spdownloader.get_answers(656155)) == 3
        assert len(self.spdownloader.get_answers(37671)) == 51
        assert len(self.spdownloader.get_answers(209015)) == 49
        assert len(self.spdownloader.get_answers(347584)) == 50
        
    def test_get_users_by_id(self):   
        assert len(self.spdownloader.get_users_by_id(130929)) == 1
        assert self.spdownloader.get_users_by_id(130929)[0]['display_name'] == 'systempuntoout'
        
    def test_get_users(self):    
        assert len(self.spdownloader.get_users('systempuntoout')) == 1
        
    def test_get_favorites_questions(self): 
        assert len(self.spdownloader.get_favorites_questions(130929, 1)[0]) > 0
        assert self.spdownloader.get_favorites_questions(130929, 1)[0][0].title !=''
        assert self.spdownloader.get_favorites_questions(130929, 1)[1].total > 0
        assert self.spdownloader.get_favorites_questions(130929, 1)[0][0].question_id > 0
        assert self.spdownloader.get_favorites_questions(130929, 1)[0][0].url.startswith('http')
        assert self.spdownloader.get_favorites_questions(130929, 1)[0][0].service != ''
        
    def test_get_tags(self):
        assert len(self.spdownloader.get_tags('python')) > 0

class MockRetriever():
    def get_question(self, question_id, api_endpoint, **kwargs):
        if question_id != 0:
            return simplejson.loads(QUESTION)
        else:
            return simplejson.loads(EMPTY_QUESTIONS)    
            
    def get_answer(self, answer_id, api_endpoint, **kwargs):
        if answer_id != 0:
            return simplejson.loads(ANSWER)
        else:
            return simplejson.loads(EMPTY_ANSWERS)
            
    def get_questions_by_tags(self, tags, api_endpoint, page, **kwargs):
        if tags == 'python':
            return simplejson.loads(QUESTIONS)
        if tags == 'atagthedoesnotexist':
            return simplejson.loads(EMPTY_QUESTIONS)
            
    def get_questions(self, api_endpoint, page, **kwargs):
        return simplejson.loads(QUESTIONS)
        
    def get_answers(self,question_id, api_endpoint, **kwargs):
        if question_id != 0:
            return simplejson.loads(ANSWERS)
        else:
            return simplejson.loads(EMPTY_ANSWERS)
        
    def get_users(self, filter, api_endpoint, **kwargs):
        return simplejson.loads(USERS)
        
    def get_users_by_id(self, user_id, api_endpoint, **kwargs):
        return simplejson.loads(USERS)
        
    def get_favorites_questions(self, user_id, api_endpoint, page, **kwargs):
        return simplejson.loads(QUESTIONS)
        
    def get_tags(self, user_id, api_endpoint, page, **kwargs):
        return simplejson.loads(TAGS)
        
if __name__ == '__main__':
    unittest.main()
