# -*- coding: utf-8 -*-
"""
Created on Sat Sep 27 14:02:40 2014

@author: harshitbahl
"""

HEADER = ['merchant','status','product','NVR','click_time','SR','transaction_time',
'MID','cash_back_amount','transaction_value','VR','transaction_date','uKey','referrer','PID','merchant_ref',
'voucher_code','transaction_id','UID']

USERHEADER = ['transaction_id','product', 'merchant', 'transaction_date', 
              'transaction_value','cash_back_amount', 'status']

USERHEADER_MAP ={'transaction_id':'Transaction ID',
                 'product':'Product Name',
                 'merchant':'Merchant Name',
                 'transaction_date':'Transaction Date',
                 'cash_back_amount': 'Cash Back Amount',
                 'transaction_value':'Transaction Value',
                 'status':'Status',}

DINING_IMAGE_MAP = {10859:"http://clk.omgt5.com/?AID=682085&PID=10859&;WID=55355",
             11313:"http://clk.omgt5.com/?AID=682085&PID=11313&WID=55355" ,
             12861:"http://clk.omgt5.com/?AID=682085&PID=12861&WID=55355" }