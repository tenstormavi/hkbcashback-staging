# -*- coding: utf-8 -*-
"""
Created on Thu Sep 18 23:49:27 2014

@author: harshitbahl
"""

from datetime import datetime
from flask import render_template, session, redirect, url_for
from . import main
from .forms import NameForm
from .. import db
from ..models import User

@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        user = collection.find_one({'name': form.name.data})
        if user is None:
            user = collection.User()
            user['name'] = form.name.data
            user['email'] = form.email.data
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