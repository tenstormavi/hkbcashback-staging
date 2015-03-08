# -*- coding: utf-8 -*-
"""
Created on Tue Sep 16 20:07:40 2014

@author: harshitbahl
"""
""" os imports """
import bson
import os
from datetime import datetime
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
from forms import ContactUs, Redeem
from forms import InputMissingTransaction
from models import User, UserTransaction, MissingTransaction, UserClickTrack


from config import MONGODB_HOST, MONGODB_PORT, COLLECTION_QA
from config import MAIL_SERVER, MAIL_PORT, MAIL_USE_TLS
from config import ENCASHMORE_MAIL_SUBJECT_PREFIX, ENCASHMORE_MAIL_SENDER, ENCASHMORE_ADMIN


from utils import validate_password, password_hash, format_transaction
from utils import get_transaction_dict, get_errors, format_Student_info, format_detail_view
from utils import format_subject_info, format_admin_transaction
from constant import USERHEADER_MAP, ORDER_MAP, STUDENT_HEADER_MAP


# Configuration
app = Flask(__name__)
app.config['DEBUG']=True
app.config.from_object(__name__)
app.config['SECRET_KEY']         = 'xcvjHJHNsnnnsHJKMNhhhhBNljhgfdvbfdgk'

# DataBase Loading
connection                       = Connection(os.environ.get('MONGOHQ_URL'))
db                               = connection[os.environ.get('COLLECTION')]
collection                       = db.users
track_collection                 = db.userClickTrack
referral_code    				           = db.referralCode

# Login Configuration
login_manager 					 = LoginManager()
login_manager.session_protection = 'strong'
login_manager.login_view         = 'login'

# Mail Configuration
app.config['MAIL_USERNAME']      = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD']      = os.environ.get('MAIL_PASSWORD')

#Other Config
bootstrap = Bootstrap(app)
manager = Manager(app)
login_manager.init_app(app)
mail = Mail(app)



# register the User document with our current connection
connection.register([User,UserTransaction, MissingTransaction, UserClickTrack])

@login_manager.user_loader
def reload_user(user_id):
    userobj = bson.objectid.ObjectId(user_id)
    return collection.User.find_one({'_id':userobj})

@app.route('/', methods=['GET', 'POST'])
def index():
    form = ContactUs()
    if form.is_submitted():
        from email_utils import send_email
        send_email(app.config['ENCASHMORE_ADMIN'], 'New Message from %s'%form.email.data,
                        'mail/contactform',
                        email=form.email.data,
                        name=form.name.data, 
                        phone = form.phonenumber.data,
                        message = form.message.data
                        )
        return redirect(request.args.get('next') or url_for('index'))
    return render_template('index.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = get_validate_user(form.email.data)
        if user and validate_password(user['password'], form.password.data):
            login_user(user, True)
            return redirect(request.args.get('next') or url_for('index'))
        flash(['Invalid username or password.'])
    else:
        if form.is_submitted():
            if form.errors:
                flash(get_errors(form))
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
                flash(['Record added successfully'])
                from email_utils import send_email
                send_email(app.config['ENCASHMORE_ADMIN'], 'Transaction added for %s'%form.email.data,
                        'mail/transaction_added', user=form.email.data)
                return redirect(url_for('transaction_form'))
            flash(['Not a valid user'])
        else:
            #TODO Need to fix this
            if form.is_submitted():
                if form.errors:
                    flash(get_errors(form))
        return render_template('transaction_form.html', form=form)
    return render_template('not_authorized.html')

@app.route('/misssingTrasaction', methods=['GET', 'POST'])
@login_required
def misssing_trasaction():
        form = InputMissingTransaction()
        if form.validate_on_submit():
            user_email = current_user.get('email')
            missing_transaction = collection.MissingTransaction()
            get_transaction_dict(missing_transaction, form)
            collection.update({'email':user_email}, {'$push': {'missingtransaction': missing_transaction}})
            flash(['Record added successfully'])
            from email_utils import send_email
            send_email(app.config['ENCASHMORE_ADMIN'], 'Missing Transaction added by %s'%user_email,
                        'mail/missing_transaction', user=user_email)
            return redirect(url_for('user_missing_transaction'))
        else:
            #TODO Need to fix this
            if form.is_submitted():
                if form.errors:
                    flash(get_errors(form))
        return render_template('missing_transaction_form.html', form=form)

@app.route('/registrationform', methods=['GET', 'POST'])
def registration_form():
    form = UserRegisteration()
    if form.validate_on_submit():
        if get_validate_user(form.email.data):
            flash(['Our Record show you are already registered please use forgot password option'])
            return render_template('login_form.html', form=form)
        if not get_valid_referralCode(form.referralcode.data):
            flash(['Invalid Referral Code Please add correct referral Code'])
            return render_template('login_form.html', form=form)
        else:
            user                 = collection.User()
            user['email']        = str(form.email.data).lower()
            user['password']     = password_hash(form.password.data)
            user['phonenumber']  = str(form.phonenumber.data)
            user['subscribed']   = form.subscription.data
            user['referralcode'] = str(form.referralcode.data)
            user.save()
            new_user_notification(user, form.email.data)
            flash('You can sign In now')
            return redirect(url_for('login'))
    else:
        if form.is_submitted():
            if form.errors:
                flash(get_errors(form))
    return render_template('login_form.html', form=form)


@app.route('/usertransactions', methods=['GET', 'POST'])
@login_required
def user_transaction():
#    user = collection.User.find_one({'email':'aashish@gmail.com'})
    user = current_user
    transaction = user.transaction
    format_info = format_transaction(transaction, header = 'user')
    user_header = [USERHEADER_MAP.get(i) for i in format_info.pop(0)]
    form = Redeem()
    if form.is_submitted():
        from email_utils import send_email
        send_email(app.config['ENCASHMORE_ADMIN'], 'Redeem Request from %s'%user.email,
                        'mail/redeem',
                        email=user.email
                        )
        flash(['We have received your redeem request we will start working on it'])
    return render_template('user_transaction.html', header = user_header,
            content = format_info, useremail = '')

@app.route('/usermissingtransactions', methods=['GET', 'POST'])
@login_required
def user_missing_transaction():
#    user = collection.User.find_one({'email':'aashish@gmail.com'})
    user = current_user
    try:
        transaction = user.missingtransaction
        format_info = format_transaction(transaction, header = 'missing')
        user_header = [USERHEADER_MAP.get(i) for i in format_info.pop(0)]
        return render_template('missing_transaction.html', header = user_header,
                               content = format_info, useremail = '')
    except AttributeError:
        return render_template('missing_transaction.html', header = None,
                               content = None, useremail = '')

@app.route('/admin/<email>', methods=['GET', 'POST'])
@login_required
def admin_user_transaction(email):
    if current_user.get('isAdmin'):
        user = collection.User.find_one({'email':email})
        transaction = user.transaction
        format_info = format_admin_transaction(transaction, header = 'user')
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
            flash(['Not a valid User %s'%form.email.data])
        else:
            #TODO Need to fix this
            if form.is_submitted():
                if form.errors:
                    flash(get_errors(form))
        return render_template('admin_search_user.html', form=form)
    return render_template('not_authorized.html')
    


@app.route('/offer/<OFFERID>')
@login_required
def offer_link(OFFERID):
    # Unicode need to be converted to int
    link_val = ORDER_MAP.get(int(OFFERID))
    if link_val:
        final_link = "%s&UID=%s"%(link_val, current_user.get_id())
        
        click                  = track_collection.UserClickTrack()
        click['userEmail']     =str(current_user.email)
        click['userUID']       =current_user.get_id()
        click['offerID']       =int(OFFERID)
        click['offerLink']     =final_link
        click['clickDateTime'] =datetime.now().isoformat(' ')
        click.save()
        return redirect(final_link)
    return render_template('invalid_offer.html')


@app.route('/offer/amazon')
@login_required
def amazon_offer_link():
    # Unicode need to be converted to int
    link_val = 'http://www.amazon.in/?&tag=682085-21'
    if link_val:
        final_link = "%s&ascsubtag=%s"%(link_val, current_user.get_id())
        
        click                  = track_collection.UserClickTrack()
        click['userEmail']     =str(current_user.email)
        click['userUID']       =current_user.get_id()
        click['offerID']       =123456
        click['offerLink']     =final_link
        click['clickDateTime'] =datetime.now().isoformat(' ')
        click.save()
        return redirect(final_link)
    return render_template('invalid_offer.html')

@app.route('/user/<UID>')
@login_required
def user(UID):
    return render_template('redirect.html',UID = UID)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route("/termcondition")
def termcondition():
    return render_template('terms_and_conditions.html')

@app.route("/faq")
def faq():
    return render_template('faq.html')

###########################################################
# Helper functions ###
                          
def get_validate_user(user_email_id):
    return collection.User.find_one({'email':user_email_id.lower()})

def get_valid_referralCode(referralcode):
    if not referralcode:
        return True
    else:
        return referral_code.find_one({'referralcode':str(referralcode)})  

def new_user_notification(user, email):
    from email_utils import send_email
    #FIX 
    send_email(app.config['ENCASHMORE_ADMIN'], 
             'New User',
             'mail/new_user', 
             user=user)
                      
    send_email([str(email)],
             'Welcome to Enchasmore',
             'mail/new_user_client')
	

if __name__ == '__main__':
    manager.run()