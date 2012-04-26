# -*- coding: utf-8 -*-

"""
Tests for db
"""

import unittest
import app.db.question as dbquestion
import logging

class QuestionTestCase(unittest.TestCase):

        
    def test_store_questions(self):
        dbquestion.store_printed_question(question_id = 1, service = 'fooservice', title = 'footitle', tags = ['tag1', 'tag2'],deleted = False)
        questions_list = dbquestion.get_top_printed_questions(1)
        self.assertEquals(len(questions_list), 1)
        self.assertEquals(questions_list[0].question_id, 1)
        dbquestion.store_printed_question(question_id = 1, service = 'fooservice', title = 'footitle', tags = ['tag1', 'tag2'],deleted = False)
        self.assertEquals(len(questions_list), 1)
        self.assertEquals(questions_list[0].question_id, 1)
        dbquestion.store_printed_question(question_id = 2, service = 'fooservice', title = 'footitle2', tags = ['tag1', 'tag2'],deleted = False)
        questions_list = dbquestion.get_top_printed_questions(1)
        self.assertEquals(len(questions_list), 2)
        self.assertEquals(questions_list[0].question_id, 1)
        self.assertEquals(questions_list[1].question_id, 2)
        dbquestion.store_printed_question(question_id = 2, service = 'fooservice', title = 'footitle2', tags = ['tag1', 'tag2'],deleted = False)
        dbquestion.store_printed_question(question_id = 2, service = 'fooservice', title = 'footitle2', tags = ['tag1', 'tag2'],deleted = False)
        questions_list = dbquestion.get_top_printed_questions(1)
        logging.debug(questions_list)
        self.assertEquals(len(questions_list), 2)
        self.assertEquals(questions_list[0].question_id, 2)
        self.assertEquals(questions_list[1].question_id, 1)
        self.assertEquals(questions_list[1].tags, ['tag1', 'tag2'])
        dbquestion.store_printed_question(question_id = 3, service = 'fooservice', title = 'footitle2', tags = ['tag1', 'tag2'],deleted = True)
        questions_list = dbquestion.get_top_printed_questions(1)
        self.assertEquals(len(questions_list), 3)
        questions_list = dbquestion.get_deleted_questions()
        self.assertEquals(len(questions_list), 1)
        
        
if __name__ == '__main__':
    unittest.main()
