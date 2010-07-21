# -*- coding: utf-8 -*-

"""
Tests for utility
"""

import unittest
from app.utility.utils import suppify_body

class UtilityTestCase(unittest.TestCase):
    def test_suppify_body(self):
        self.assertTrue(str(suppify_body('<a href="http://www.foo.it">foo</a>')[0]).endswith('</a><sup style="font-size:9px">[1]</sup>') )
        self.assertTrue(str(suppify_body('<a href="http://www.foo.it">http://www.foo.it</a>')[0]) == '<a href="http://www.foo.it">http://www.foo.it</a>' )
        self.assertEquals(suppify_body('<a href="http://www.foo.it">foo</a>')[1], {1: u'http://www.foo.it'})
        self.assertEquals(suppify_body('<a href="http://www.foo.it"><h>foo</h></a>')[1], {1: u'http://www.foo.it'})
        self.assertEquals(suppify_body('<a href="http://www.foo.it">http://www.foo.it</a>')[1], {})
        self.assertEquals(suppify_body('<a href="">http://www.foo.it</a>')[1], {})
        self.assertEquals(suppify_body('<a hrek="http://www.foo.it">foo</a>')[1], {})

if __name__ == '__main__':
    unittest.main()
