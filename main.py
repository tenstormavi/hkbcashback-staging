# -*- coding: utf-8 -*-
"""
Created on Tue Sep 16 20:07:40 2014

@author: harshitbahl
"""
""" os imports """
import bson
import os
""" flask and flask extensions"""
from flask import Flask, render_template,session, redirect, url_for, flash
from flask import request
from flask.ext.bootstrap import Bootstrap
from flask.ext.login import login_user, logout_user, login_required
from flask.ext.login import LoginManager, current_user
from flask.ext.script import Manager
from flask.ext.mail import Mail
"""DB Releated """
from mongokit import Connection
""" Custom Modules """
from forms import LoginForm, InputTransaction, UserRegisteration, SearchUser
from models import User, UserTransaction

from config import MONGODB_HOST, MONGODB_PORT, COLLECTION_QA
from config import MAIL_SERVER, MAIL_PORT, MAIL_USE_TLS
from config import ENCASHMORE_MAIL_SUBJECT_PREFIX, ENCASHMORE_MAIL_SENDER, ENCASHMORE_ADMIN


from utils import validate_password, password_hash, format_transaction
from utils import get_transaction_dict
from constant import USERHEADER_MAP


# configuration
app = Flask(__name__)
app.config['DEBUG']=True
app.config.from_object(__name__)
app.config['SECRET_KEY'] = 'xcvjHJHNsnnnsHJKMNhhhhBN'
connection = Connection(os.environ.get('MONGOHQ_URL'))
db = connection[os.environ.get('COLLECTION')]
collection = db.users
login_manager = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view = 'login'
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
bootstrap = Bootstrap(app)
manager = Manager(app)
login_manager.init_app(app)
mail = Mail(app)



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
        user = get_validate_user(form.email.data)
        if user and validate_password(user['password'], form.password.data):
            login_user(user, True)
            return redirect(request.args.get('next') or url_for('index'))
        flash('Invalid username or password.')
    return render_template('Login.html', form=form)

@app.route('/transactionForm', methods=['GET', 'POST'])
@login_required
def transaction_form():
    if current_user.get('isAdmin'):
        form = InputTransaction()
        if form.validate_on_submit():
            transaction = collection.UserTransaction()
            if get_validate_user(form.email.data):
                get_transaction_dict(transaction, form)
                collection.update({'email':form.email.data}, {'$push': {'transaction': transaction}})
                flash('Record added successfully')
                from email_utils import send_email
                send_email(app.config['ENCASHMORE_ADMIN'], 'Transaction added for %s'%form.email.data,
                        'mail/transaction_added', user=user)
                return redirect(url_for('transaction_form'))
            flash('Not a valid user')
        return render_template('transaction_form.html', form=form)
    return render_template('not_authorized.html')

@app.route('/registrationform', methods=['GET', 'POST'])
def registration_form():
    form = UserRegisteration()
    if form.validate_on_submit():
#        user = collection.User.find_one({'email':form.email.data})
        if not get_validate_user(form.email.data):
            user = collection.User()
            user['email'] = str(form.email.data)
            user['password']= password_hash(form.password.data)
            user['phonenumber']= str(form.phonenumber.data)
            user['subscribed']  = form.subscription.data
            user.save()
            
            from email_utils import send_email
            send_email(app.config['ENCASHMORE_ADMIN'], 'New User',
                        'mail/new_user', user=user)
                        
            flash('You can sign In now')
            return redirect(url_for('login'))
        flash('Our Record show you are already registered please use forgot password option')
    else:
        #TODO Need to fix this
        if form.is_submitted():
            if form.errors:
                flash('Please input correct values')
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
            content = format_info, useremail = '')

@app.route('/admin/<email>', methods=['GET', 'POST'])
@login_required
def admin_user_transaction(email):
    if current_user.get('isAdmin'):
        user = collection.User.find_one({'email':email})
        transaction = user.transaction
        format_info = format_transaction(transaction)
        user_header = [USERHEADER_MAP.get(i) for i in format_info.pop(0)]
        return render_template('user_transaction.html', header = user_header,
                content = format_info, useremail=email)
    return render_template('not_authorized.html')

@app.route('/findtransaction', methods=['GET', 'POST'])
@login_required
def admin_search_transaction():
    if current_user.get('isAdmin'):
        form =SearchUser()
        if form.validate_on_submit():
            if get_validate_user(form.email.data):
                return redirect(url_for('admin_user_transaction', email=form.email.data, method=['GET', 'POST']))
            flash('Not a valid User %s'%form.email.data)
        else:
            #TODO Need to fix this
            if form.is_submitted():
                if form.errors:
                    flash(form.errors)
        return render_template('admin_search_user.html', form=form)
    return render_template('not_authorized.html')
    



@app.route('/user/<UID>')
@login_required
def user(UID):
    return render_template('redirect.html',UID = UID)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

def get_validate_user(user_email_id):
    return collection.User.find_one({'email':user_email_id})

if __name__ == '__main__':
    manager.run()