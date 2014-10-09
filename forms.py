# -*- coding: utf-8 -*-
"""
Created on Sun Sep 21 22:01:41 2014

@author: harshitbahl
"""
from wtforms import StringField, SubmitField, PasswordField, DateTimeField
from wtforms import BooleanField, IntegerField
from wtforms import FloatField
from flask.ext.wtf import Form
from wtforms.validators import Required, Email, Length, any_of, EqualTo, Regexp,NumberRange

class NameForm(Form):
    name = StringField('What is your name?', validators=[Required()])
    email = StringField('What is your Email?', validators=[Required()])
    submit = SubmitField('Submit')

class LoginForm(Form):
    email = StringField('Email', validators=[Required(), Length(1, 64),
                                             Email()])
    password = PasswordField('Password', validators=[Required()])
#    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')

class UserRegisteration(Form):
    email = StringField('Email', validators=[Required(), Length(1, 64),
                                             Email()])
    password = PasswordField('Password', validators=[Required(), 
                        EqualTo('password2', message='Passwords must match.')])
    password2 = PasswordField('Confirm password', validators=[Required()])
    phonenumber = StringField('Phone Number', validators=[Required(),Regexp(r'^[789]\d{9}$', message='Not valid Phone Number')])
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
    merchant = StringField('Merchant Name', validators=[Required()])
#    PID = StringField('PID', validators=[Required()])
    product = StringField('Product Name', validators=[Required()])
    referrer = StringField('Referred By')
#    SR = DecimalField('SR')
#    VR = DecimalField('VR')
#    NVR = DecimalField('NVR')
    status  = StringField('Status', validators=[Required()])
    cash_back_amount  = FloatField('Cash Back Amount')
#    uKey  = StringField('uKey', validators=[Required()])
    transaction_value  = FloatField('Transaction Value')
    voucher_code  = StringField('Voucher Code')
    
    submit = SubmitField('Submit')

                                          
class SearchUser(Form):
    email = StringField('User Email', validators=[Required(), Length(1, 64),
                                             Email()])
    submit = SubmitField('Submit')