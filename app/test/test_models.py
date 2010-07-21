# -*- coding: utf-8 -*-

"""
Tests for models
"""

import unittest
from app.models.pagination import Pagination

class PaginationTestCase(unittest.TestCase):
    def test_get_pretty_pagination(self):
        result = {'total':10,'page':1,'pagesize':30}
        self.assertEquals(Pagination(result).get_pretty_pagination(), [])
        result = {'total':40,'page':1,'pagesize':30}
        self.assertEquals(Pagination(result).get_pretty_pagination(), [1,2])
        result = {'total':100,'page':1,'pagesize':10}
        self.assertEquals(Pagination(result).get_pretty_pagination(), [1, 2, 3, -1, 10])
        result = {'total':100,'page':2,'pagesize':10}
        self.assertEquals(Pagination(result).get_pretty_pagination(), [1, 2, 3, -1, 10])
        result = {'total':100,'page':3,'pagesize':10}
        self.assertEquals(Pagination(result).get_pretty_pagination(), [1, 2, 3, 4, -1, 10])
        result = {'total':100,'page':4,'pagesize':10}
        self.assertEquals(Pagination(result).get_pretty_pagination(), [1, -1, 3, 4, 5, -1, 10])
        result = {'total':100,'page':5,'pagesize':10}
        self.assertEquals(Pagination(result).get_pretty_pagination(), [1, -1, 4, 5, 6, -1, 10])
        result = {'total':100,'page':6,'pagesize':10}
        self.assertEquals(Pagination(result).get_pretty_pagination(), [1, -1, 5, 6, 7, -1, 10])
        result = {'total':100,'page':7,'pagesize':10}
        self.assertEquals(Pagination(result).get_pretty_pagination(), [1, -1, 6, 7, 8, -1, 10])
        result = {'total':100,'page':8,'pagesize':10}
        self.assertEquals(Pagination(result).get_pretty_pagination(), [1, -1, 7, 8, 9, 10])
        result = {'total':100,'page':9,'pagesize':10}
        self.assertEquals(Pagination(result).get_pretty_pagination(), [1, -1, 8, 9 , 10])
        result = {'total':100,'page':10,'pagesize':10}
        self.assertEquals(Pagination(result).get_pretty_pagination(), [1, -1, 8, 9 , 10])
    def test_total_pages(self):
        result = {'total':0,'page':1,'pagesize':10}
        self.assertEquals(Pagination(result).total_pages, 0)
        result = {'total':9,'page':1,'pagesize':10}
        self.assertEquals(Pagination(result).total_pages, 1)
        result = {'total':10,'page':1,'pagesize':10}
        self.assertEquals(Pagination(result).total_pages, 1)
        result = {'total':11,'page':1,'pagesize':10}
        self.assertEquals(Pagination(result).total_pages, 2)
        result = {'total':19,'page':1,'pagesize':10}
        self.assertEquals(Pagination(result).total_pages, 2)
        result = {'total':20,'page':1,'pagesize':10}
        self.assertEquals(Pagination(result).total_pages, 2)
        result = {'total':21,'page':1,'pagesize':10}
        self.assertEquals(Pagination(result).total_pages, 3)

if __name__ == '__main__':
    unittest.main()
