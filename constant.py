# -*- coding: utf-8 -*-
"""
Created on Sat Sep 27 14:02:40 2014

@author: harshitbahl
"""

HEADER = ['merchant', 'status', 'product', 'NVR', 'click_time', 'SR', 'transaction_time',
			  'MID', 'cash_back_amount', 'transaction_value', 'VR', 'transaction_date',
			  'uKey', 'referrer', 'PID', 'merchant_ref', 'voucher_code', 'transaction_id','UID']

USERHEADER = ['transaction_id', 'product', 'merchant', 'transaction_date', 
              'transaction_value', 'cash_back_amount', 'status']

USERHEADER_MAP ={'transaction_id'   :'Transaction ID',
                 'product'          :'Product Name',
                 'merchant'         :'Merchant Name',
                 'transaction_date' :'Transaction Date',
                 'cash_back_amount' : 'Cash Back Amount',
                 'transaction_value':'Transaction Value',
                 'status'           :'Status',
                 'merchant_ref'     : 'Merchant Ref',
                 'email'            :'Username',
                 'password'         :'Password',
                 'password2'        :'Password',
                 'phonenumber'      :'Phone Number'
                 }
                 
MISSING_HEADER = ['transaction_date', 'merchant_ref', 'merchant', 'product',  
                  'transaction_value', 'cash_back_amount', 'status']

STUDENT_HEADER = ['FirstName', 'LastName', 'AverageGrade', 'ViewAdditionalInfo']

STUDENT_INFO_HEADER = ['FirstName', 'LastName', 'EmailAddress', 'AverageGrade']

SUBJECT_INFO_HEADER = ['SubjectName', 'Marks']

STUDENT_HEADER_MAP = {'FirstName':'First Name',
                      'LastName' : 'Last Name',
                      'AverageGrade': 'Average Grade',
                      'ViewAdditionalInfo': 'View Additional Info',
                      'EmailAddress':'Email Address',
                      'SubjectName': 'Subject Name',
                      'Marks':'Marks'
                      }


ORDER_MAP = {10859:"http://clk.omgt5.com/?AID=682085&PID=10859&WID=55355",
             11313:"http://clk.omgt5.com/?AID=682085&PID=11313&WID=55355" ,
             12861:"http://clk.omgt5.com/?AID=682085&PID=12861&WID=55355" ,
             11897:"http://clk.omgt5.com/?AID=682085&PID=11897&WID=55355",
             11898:"http://clk.omgt5.com/?AID=682085&PID=11898&WID=55355",
             11896:"http://clk.omgt5.com/?AID=682085&PID=11896&WID=55355",
             13298:"http://clk.omgt5.com/?AID=682085&PID=13298&WID=55355",
             9807:"http://clk.omgt5.com/?AID=682085&PID=9807&WID=55355",
             10332:"http://clk.omgt5.com/?AID=682085&PID=10332&WID=55355",
             11446:"http://clk.omgt3.com/?AID=682085&PID=11446&WID=55355",
             9401:"http://clk.omgt5.com/?AID=682085&PID=9401&WID=55355",
             10940:"http://clk.omgt5.com/?AID=682085&PID=10940&WID=55355",
             13495:"http://clk.omgt5.com/?AID=682085&PID=13495&WID=55355",
             7970:"http://clk.omgt5.com/?AID=682085&PID=7970&WID=55355",
             9394:"http://clk.omgt5.com/?AID=682085&PID=9394&WID=55355",
            10359:"http://clk.omgt5.com/?AID=682085&PID=10359&WID=55355",
            8053:"http://clk.omgt5.com/?AID=682085&PID=8053&WID=55355",
            12185:"http://clk.omgt5.com/?AID=682085&PID=12185&WID=55355",
            8422:"http://clk.omgt5.com/?AID=682085&PID=8422&WID=55355",
            13171:"http://clk.omgt5.com/?AID=682085&PID=13171&WID=55355",
            12957:"http://clk.omgt5.com/?AID=682085&PID=12957&WID=55355",
            9222:"http://clk.omgt5.com/?AID=682085&PID=9222&WID=55355",
            9170:"http://clk.omgt5.com/?AID=682085&PID=9170&WID=55355",
            10109:"http://clk.omgt5.com/?AID=682085&PID=10109&WID=55355",
            9828:"http://clk.omgt5.com/?AID=682085&PID=9828&WID=55355",
            11365:"http://clk.omgt5.com/?AID=682085&PID=11365&WID=55355",
            11289:"http://clk.omgt5.com/?AID=682085&PID=11289&WID=55355",
            11010:"http://clk.omgt5.com/?AID=682085&PID=11010&WID=55355",
            11365:"http://clk.omgt5.com/?AID=682085&PID=11365&WID=55355",
            9319:"http://clk.omgt5.com/?AID=682085&PID=9319&WID=55098",
            12429:"http://clk.omgt5.com/?AID=682085&PID=12429&WID=55355",
            13255:"http://clk.omgt5.com/?AID=682085&PID=13255&WID=55355",
            11965:"http://clk.omgt5.com/?AID=682085&PID=11965&WID=55355",
            10036:"http://clk.omgt5.com/?AID=682085&PID=10036&WID=55355",
            12185:"http://clk.omgt5.com/?AID=682085&PID=12185&WID=55355",
            12495:"http://clk.omgt5.com/?AID=682085&PID=12495&WID=55355",
            11482:"http://clk.omgt5.com/?AID=682085&PID=11482&WID=55355",
             }
