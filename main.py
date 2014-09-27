# -*- coding: utf-8 -*-
"""
Created on Tue Sep 16 20:07:40 2014

@author: harshitbahl
"""

from flask import Flask, render_template,session, redirect, url_for, flash
from flask import request
from flask.ext.bootstrap import Bootstrap
from mongokit import Connection
from flask.ext.login import login_user, logout_user

from flask.ext.script import Manager

from config import MONGODB_HOST, MONGODB_PORT, COLLECTION_QA
from forms import NameForm, LoginForm, InputTransaction, UserRegisteration
from models import User, UserTransaction
from utils import validate_password, password_hash
from flask.ext.login import LoginManager
# configuration
app = Flask(__name__)
app.config.from_object(__name__)
app.config['SECRET_KEY'] = 'xcvjHJHNsnnnsHJKMNhhhhBN'
connection = Connection(app.config['MONGODB_HOST'],
                        app.config['MONGODB_PORT'])
db = connection[COLLECTION_QA]

collection = db.users

def reload_user(user_id):
   return collection.User.find_one({'_id':user_id})

login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'auth.login'
login_manager.user_callback = reload_user
bootstrap = Bootstrap(app)
manager = Manager(app)
login_manager.init_app(app)



# register the User document with our current connection
connection.register([User,UserTransaction])

@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = collection.find_one({'name': form.name.data})
        if user is None:
            user = collection.User()
            user['name'] = form.name.data
            user['password'] = form.password.data
            collection.insert(user)
            session['known'] = False
        else:
            session['known'] = True
        session['name'] = form.name.data
        form.name.data = ''
        return redirect(url_for('index'))
    return render_template('index.html',
        form = form, name = session.get('name'),
        known = session.get('known', False))

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = collection.User.find_one({'email':form.email.data})
        if user and validate_password(user['password'], form.password.data):
            login_user(user)
            return redirect(url_for('user', UID = user.get_id()))
        flash('Invalid username or password.')
    return render_template('login.html', form=form)

@app.route('/transactionForm', methods=['GET', 'POST'])
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
            transaction['paid'] = form.paid.data
            transaction['transaction_value']= form.transaction_value.data
            transaction['voucher_code']= form.voucher_code.data
            collection.update({'email':form.email.data}, {'$push': {'transaction': transaction}})
            return redirect(url_for('browser_info'))
        flash('Not a valid user')
    return render_template('transaction_form.html', form=form)

@app.route('/loginform', methods=['GET', 'POST'])
def login_form():
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
            return redirect(url_for('browser_info'))
        flash('Our Record show you are already registered please use forgot password option')
    return render_template('login_form.html', form=form)
        
        
        

@app.route('/user/<UID>')
def user(UID):
    return render_template('redirect.html',UID = UID)
    
@app.route('/browserinfo')
def browser_info():
    return render_template('logout.html')

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('browser_info'))

if __name__ == '__main__':
    manager.run()