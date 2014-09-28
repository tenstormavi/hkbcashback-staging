# -*- coding: utf-8 -*-
"""
Created on Sun Sep 21 22:10:12 2014

@author: harshitbahl
"""

from werkzeug.security import generate_password_hash, check_password_hash
from constant import HEADER, USERHEADER

def max_length(length):
    def validate(value):
        if len(value) <= length:
            return True
        raise Exception('%s must be at most %s characters long' % length)
    return validate

def password_hash(password):
    return generate_password_hash(password)

def validate_password(password_hash, password):
    return check_password_hash(password_hash, password)

def valid_status(status):
    def valid(value):
        if [value] in status:
            return  True
        raise Exception('Not Valid Value Valid Values Paid or Not Paid')
    return valid

def update_user_transaction(collection):
    return 

def format_transaction(transactions):
    rst = []
    rst.append(USERHEADER)
    for transaction in transactions:
        rst.append([str(transaction.get(val)) for val in USERHEADER])
    return rst
        