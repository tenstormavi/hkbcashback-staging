# -*- coding: utf-8 -*-
"""
Created on Sun Sep 21 22:01:41 2014

@author: harshitbahl
"""
from wtforms import StringField, SubmitField, PasswordField, DateTimeField
from wtforms import BooleanField, IntegerField
from wtforms import FloatField
from flask.ext.wtf import Form
from wtforms.validators import Required, Email, Length, any_of

class NameForm(Form):
    name = StringField('What is your name?', validators=[Required()])
    email = StringField('What is your Email?', validators=[Required()])
    submit = SubmitField('Submit')

class LoginForm(Form):
    email = StringField('email', validators=[Required(), Length(1, 64),
                                             Email()])
    password = PasswordField('Password', validators=[Required()])
#    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')

class UserRegisteration(Form):
    email = StringField('email', validators=[Required(), Length(1, 64),
                                             Email()])
    password = PasswordField('Password', validators=[Required()])
    phonenumber = IntegerField('Phone Number', validators=[Required()])
    subscription = BooleanField('Email Subscription')
    submit = SubmitField('Submit')
    
    
    

class InputTransaction(Form):
    email = StringField('User Email', validators=[Required(), Length(1, 64),
                                             Email()])
    click_time = StringField('Click Time', validators=[Required()])
    transaction_time = StringField('Transaction Time', validators=[Required()])
    transaction_date = StringField('Transaction Date', validators=[Required()])
    transaction_id = StringField('Transaction ID', validators=[Required()])
    merchant_ref = StringField('Merchant Ref', validators=[Required()])
#    UID:StringField('UID', validators=[Required()])
#    MID = StringField('MID', validators=[])
    merchant = StringField('Merchant', validators=[Required()])
#    PID = StringField('PID', validators=[Required()])
    product = StringField('Product', validators=[Required()])
    referrer = StringField('Referrer', validators=[Required()])
#    SR = DecimalField('SR')
#    VR = DecimalField('VR')
#    NVR = DecimalField('NVR')
    status  = StringField('Status', validators=[Required()])
    paid  = FloatField('Paid Value')
#    uKey  = StringField('uKey', validators=[Required()])
    transaction_value  = FloatField('Transaction Value')
    voucher_code  = StringField('voucher_code', validators=[Required()])
    
    submit = SubmitField('Submit')

                                          
    