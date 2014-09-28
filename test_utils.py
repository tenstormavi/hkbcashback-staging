# -*- coding: utf-8 -*-
"""
Created on Sat Sep 27 14:08:12 2014

@author: harshitbahl
"""
import unittest
from utils import format_transaction

class Testshowtransaction(unittest.TestCase):
    
   def setUp(self):
       self.input = [{u'merchant': u'Amazon', u'status': u'Not Paid', 
                       u'product': u'Iphone', u'NVR': None,
                       u'click_time': u'12:34', u'SR': None,
                       u'transaction_time': u'12:34', u'MID': None,
                       u'paid': 20.0, u'transaction_value': 2000.0,
                       u'VR': None, u'transaction_date': u'03-03-2015',
                       u'uKey': None, u'referrer': u'Ashi',
                       u'merchant_ref': u'234', u'UID': None,
                       u'voucher_code': u'HJKN', 
                       u'transaction_id': u'1234HJN', u'PID': None}]
   
   def test_positiveTest(self):
       output = format_transaction(self.input)
       self.assertEqual('Amazon', output[1][0])


if __name__ == '__main__':
    unittest.main()
       
        