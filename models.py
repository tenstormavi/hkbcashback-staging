# -*- coding: utf-8 -*-
"""
Created on Sun Sep 21 22:07:11 2014

@author: harshitbahl
"""
from flask.ext.login import UserMixin, current_app
from mongokit import Document
from utils import max_length, valid_status
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
import bson


class User(Document, UserMixin):
    __collection__ = 'users'
    __database__ = 'cashBackPlatform'
    structure = {
        'name':str,
        'email': str,
        'password': str,
        'transaction':list,
        'missingtransaction':list,
        'phonenumber':str,
        'subscribed':bool,
        'isAdmin':bool,
        'referralcode':str,
    }
    validators = {
        'email': max_length(50),
    }
    
    default_values = {'isAdmin':False}
    
    use_dot_notation = True
    
    def get_id(self):
        return self._id.__str__()
    
    def isadmin(self):
        return self.isadmin
        
    def __repr__(self):
        return '<User %s>' % (self.email)

    def get_token(self, expiration=1800):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'user': self.get_id()}).decode('utf-8')

    @staticmethod
    def verify_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return None
        id = data.get('user')
        if id:
            return bson.objectid.ObjectId(id)
        return None

class UserTransaction(Document):
    structure = {
    'click_time':str,
    'transaction_time':str,
    'transaction_date':str,
    'transaction_id':str,
    'merchant_ref':str,
    'UID':str,
    'MID':str,
    'merchant':str,
    'PID':str,
    'product':str,
    'referrer':str,
    'SR':float,
    'VR':float,
    'NVR':float,
    'status':str,
    'cash_back_amount':float,
    'uKey':str,
    'transaction_value':float,
    'voucher_code':str,
        }
    
    validators = {
        'status': valid_status(['Paid','Not Paid']),
    }
    def __repr__(self):
        return '<product %s>' % (self.product)

class MissingTransaction(Document):
    structure = {
    'transaction_time':str,
    'transaction_date':str,
    'merchant_ref':str,
    'merchant':str,
    'product':str,
    'status':str,
    'cash_back_amount':float,
    'transaction_value':float,
        }
    
    validators = {
        'status': valid_status(['Paid','Not Paid']),
    }
    def __repr__(self):
        return '<product %s>' % (self.product)
    
class UserClickTrack(Document):
    structure = {
    'userEmail':str,
    'userUID':str,
    'offerID':int,
    'clickDateTime':str,
    'offerLink':str,
        }
    
    validators = {
    }
    def __repr__(self):
        return '<UserEmail %s>' % (self.UserEmail)

    