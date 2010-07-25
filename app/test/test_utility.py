# -*- coding: utf-8 -*-

"""
Tests for utility
"""

import unittest
from app.utility.utils import suppify_body
from app.utility.utils import order_supported_services_keys
from app.utility.utils import Pagination

class UtilityTestCase(unittest.TestCase):
    def test_suppify_body(self):
        self.assertTrue(str(suppify_body('<a href="http://www.foo.it">foo</a>')[0]).endswith('</a><sup style="font-size:9px">[1]</sup>') )
        self.assertTrue(str(suppify_body('<a href="http://www.foo.it">http://www.foo.it</a>')[0]) == '<a href="http://www.foo.it">http://www.foo.it</a>' )
        self.assertEquals(suppify_body('<a href="http://www.foo.it">foo</a>')[1], {1: u'http://www.foo.it'})
        self.assertEquals(suppify_body('<a href="http://www.foo.it"><h>foo</h></a>')[1], {1: u'http://www.foo.it'})
        self.assertEquals(suppify_body('<a href="http://www.foo.it">http://www.foo.it</a>')[1], {})
        self.assertEquals(suppify_body('<a href="">http://www.foo.it</a>')[1], {})
        self.assertEquals(suppify_body('<a hrek="http://www.foo.it">foo</a>')[1], {})

    def test_order_supported_services_keys(self):
        supported_services_keys = ['white.stackexchange','meta.white.stackexchange','stackoverflow','meta.stackoverflow','serverfault','meta.serverfault','superuser','meta.superuser','stackapps'\
                                   ,'blu.stackexchange','meta.blu.stackexchange','red.stackexchange','meta.red.stackexchange']
        supported_services_keys_ordered = ['stackoverflow','superuser','serverfault','stackapps','meta.stackoverflow','meta.serverfault','meta.superuser', \
                                          'blu.stackexchange','meta.blu.stackexchange','red.stackexchange','meta.red.stackexchange','white.stackexchange','meta.white.stackexchange']                           
        self.assertEquals(order_supported_services_keys(supported_services_keys), supported_services_keys_ordered)                                  


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
