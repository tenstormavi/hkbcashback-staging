# -*- coding: utf-8 -*-
"""
Created on Mon Oct 13 00:27:31 2014

@author: harshitbahl
"""

import os
import main
import unittest
import tempfile

class FlaskrTestCase(unittest.TestCase):

    def setUp(self):
        self.db_fd, main.app.config['DATABASE'] = tempfile.mkstemp()
        main.app.config['TESTING'] = True
        self.app = main.app.test_client()
#        main.init_db()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(main.app.config['DATABASE'])


    def test_empty_db(self):
        rv = self.app.get('/')
        print rv.data
        assert 'No entries here so far' in rv.data

if __name__ == '__main__':
    unittest.main()