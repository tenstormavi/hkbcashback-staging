# -*- coding: utf-8 -*-
"""
Created on Tue Sep 16 20:07:40 2014

@author: harshitbahl
"""

import bson
import os
from flask import Flask, render_template,session, redirect, url_for, flash
from flask import request
from flask.ext.bootstrap import Bootstrap
from mongokit import Connection
from flask.ext.login import login_user, logout_user, login_required
from flask.ext.login import LoginManager, current_user

from flask.ext.script import Manager

from config import MONGODB_HOST, MONGODB_PORT, COLLECTION_QA
from forms import LoginForm, InputTransaction, UserRegisteration
from models import User, UserTransaction
from utils import validate_password, password_hash, format_transaction
from constant import USERHEADER_MAP
# configuration
app = Flask(__name__)
app.config['DEBUG']=True
app.config.from_object(__name__)
app.config['SECRET_KEY'] = 'xcvjHJHNsnnnsHJKMNhhhhBN'
#connection = Connection(app.config['MONGODB_HOST'],
#                        app.config['MONGODB_PORT'])
connection = Connection(os.environ.get('MONGOHQ_URL'))
db = connection[os.environ.get('COLLECTION')]

collection = db.users



login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'
#login_manager.user_callback = reload_user
bootstrap = Bootstrap(app)
manager = Manager(app)
login_manager.init_app(app)



# register the User document with our current connection
connection.register([User,UserTransaction])

@login_manager.user_loader
def reload_user(user_id):
    userobj = bson.objectid.ObjectId(user_id)
    return collection.User.find_one({'_id':userobj})

@app.route('/', methods=['GET', 'POST'])
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = collection.User.find_one({'email':form.email.data})
        if user and validate_password(user['password'], form.password.data):
            login_user(user, True)
            return redirect(request.args.get('next') or url_for('index'))
        flash('Invalid username or password.')
    return render_template('Login.html', form=form)

@app.route('/transactionForm', methods=['GET', 'POST'])
@login_required
def transaction_form():
    form = InputTransaction()
    if form.validate_on_submit():
        transaction = collection.UserTransaction()
        user = collection.User.find_one({'email':form.email.data})
        if user:
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
            collection.update({'email':form.email.data}, {'$push': {'transaction': transaction}})
            flash('Record added successfully')            
            return redirect(url_for('transaction_form'))
        flash('Not a valid user')
    return render_template('transaction_form.html', form=form)

@app.route('/registrationform', methods=['GET', 'POST'])
def registration_form():
    form = UserRegisteration()
    if form.validate_on_submit():
        user = collection.User.find_one({'email':form.email.data})
        if not user:
            user = collection.User()
            user['email'] = str(form.email.data)
            user['password']= password_hash(form.password.data)
            user['phonenumber']= form.phonenumber.data
            user['subscribed']  = form.subscription.data
            user.save()
            flash('You can sign In now')
            return redirect(url_for('login'))
        flash('Our Record show you are already registered please use forgot password option')
    return render_template('login_form.html', form=form)

@app.route('/usertransactions', methods=['GET', 'POST'])
@login_required
def user_transaction():
#    user = collection.User.find_one({'email':'aashish@gmail.com'})
    user = current_user
    transaction = user.transaction
    format_info = format_transaction(transaction)
    user_header = [USERHEADER_MAP.get(i) for i in format_info.pop(0)]
    return render_template('user_transaction.html', header = user_header,
            content = format_info)
        

@app.route('/user/<UID>')
@login_required
def user(UID):
    return render_template('redirect.html',UID = UID)
    
@app.route('/goodbyemessage')
def goodbyemessage():
    return render_template('logout.html')

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('goodbyemessage'))

if __name__ == '__main__':
    manager.run()