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

def format_transaction(transactions):
    rst = []
    rst.append(USERHEADER)
    for transaction in transactions:
        rst.append([str(transaction.get(val)) for val in USERHEADER])
    return rst

def get_transaction_dict(transaction, form):
    transaction['click_time'] = form.click_time.data
    transaction['transaction_time'] = form.transaction_time.data
    transaction['transaction_date'] = form.transaction_date.data
    transaction['transaction_id'] = form.transaction_id.data
    transaction['merchant_ref'] = form.merchant_ref.data
    transaction['merchant'] =  form.merchant.data
    transaction['product'] = form.product.data
    transaction['referrer'] = form.referrer.data
    transaction['status'] = form.status.data
    transaction['cash_back_amount'] = form.cash_back_amount.data
    transaction['transaction_value']= form.transaction_value.data
    transaction['voucher_code']= form.voucher_code.data
    return transaction
    
        