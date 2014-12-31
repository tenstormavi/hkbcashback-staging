# -*- coding: utf-8 -*-
"""
Created on Sun Sep 21 22:10:12 2014

@author: harshitbahl
"""

from werkzeug.security import generate_password_hash, check_password_hash
from constant import HEADER, USERHEADER, MISSING_HEADER, USERHEADER_MAP, STUDENT_HEADER
from constant import STUDENT_INFO_HEADER, SUBJECT_INFO_HEADER
from datetime import datetime
from wtforms.validators import ValidationError

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

def format_transaction(transactions, header):
    rst = []
    if header == 'user':
        rst.append(USERHEADER)
        header = USERHEADER            
    else:
        rst.append(MISSING_HEADER)
        header = MISSING_HEADER
    for transaction in transactions:
        rst.append([str(transaction.get(val)) for val in header])
    return rst

def format_admin_transaction(transactions, header):
    rst = []
    if header == 'user':
        rst.append(USERHEADER)
        header = USERHEADER            
    else:
        rst.append(MISSING_HEADER)
        header = MISSING_HEADER
    for transaction in transactions:
        data = [str(transaction.get(val)) for val in header]
        data.append('<strong><a style="color: #FFF" href="%s/%s">Click Here</a></strong>'%('adminAction',str(transaction.get('transaction_id'))))
        rst.append(data)
    return rst


def format_Student_info(infos):
    rst = []
    rst.append(STUDENT_HEADER)
    header = STUDENT_HEADER
    avg = [get_average(i.get('Subjects').values()) for i in infos] 
    for info,a in zip(infos,avg):
        info['AverageGrade']=a
        info['ViewAdditionalInfo']='<strong><a style="color: #FFF" href="%s/%s">Click Here</a></strong>'%('SearchStudentInfo',str(info.get('_id')))
    for info in infos:
        rst.append([str(info.get(val)) for val in header])
    return rst

def format_detail_view(infos):
    rst = []
    rst.append(STUDENT_INFO_HEADER)
    header = STUDENT_INFO_HEADER
    avg = [get_average(i.get('Subjects').values()) for i in infos] 
    for info,a in zip(infos,avg):
        info['AverageGrade']=a
    for info in infos:
        rst.append([str(info.get(val)) for val in header])
    return rst

def format_subject_info(info):
    rst = []
    rst.append(SUBJECT_INFO_HEADER)
    header = SUBJECT_INFO_HEADER
    rst.append([str(info.get(val)) for val in header])
    return rst
    
    
    

def get_average(data):
    return round(sum(data)/len(data), 1)

def get_transaction_dict(transaction, form):
    for label, value in form.data.iteritems():
        transaction[label]=value
    return transaction

def get_errors(form):
    return ['Error in "%s" %s'%(USERHEADER_MAP.get(field), error[0])for field, error in form.errors.iteritems()]

def missing_transaction_validation(form, field):
    transaction_date =datetime.strptime(field.data, "%m/%d/%Y %I:%M %p")
    time_delta = datetime.now() - transaction_date
    if time_delta.days < 2:
        raise ValidationError('Ticket can only be raised after 72 hrs of order')
    
        