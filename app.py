#!/usr/bin/env python3

import os
import logging as log

from functools import wraps
from random import choice
from flask import Flask, session, url_for, flash, redirect, request, render_template
from flask_oauthlib.client import OAuth
from hsapi import HSApi

log.basicConfig(level=log.DEBUG)

app = Flask(__name__)
app.secret_key = 'dev secret key horses hippos misssspellings etc'

auth = OAuth(app).remote_app(
    'hackerschool'
    , base_url         = 'https://www.hackerschool.com/api/v1/'
    , access_token_url = 'https://www.hackerschool.com/oauth/token'
    , authorize_url    = 'https://www.hackerschool.com/oauth/authorize'
    , consumer_key     = os.environ.get('CONSUMER_KEY', None)
    , consumer_secret  = os.environ.get('CONSUMER_SECRET', None)
    , access_token_method='POST'
    )

hsapi = HSApi(auth)

def get_login():
    login = session.get('login')
    log.debug('retrieving login %s', login)
    return login

@auth.tokengetter
def get_token(token=None):
    token = get_login()['oauth_token']
    log.debug('retrieving token %s', token)
    return token

def protected(route):
    @wraps(route)
    def wrapper(*args, **kwargs):
        kwargs.update(login=get_login())
        return route(*args, **kwargs) if kwargs['login'] \
            else redirect(url_for('login', next=request.url))
    return wrapper

@app.route('/login')
def login():
    if get_login():
        flash('You are already logged in.')
        return redirect(request.referrer or url_for('index'))
    else:
        afterward = request.args.get('next') or request.referrer or None
        landing = url_for('oauth_authorized', next=afterward, _external=True)
        return auth.authorize(callback=landing)

@app.route('/oauth_authorized')
@auth.authorized_handler
def oauth_authorized(resp):
    try:
        # make a partial login session here, get the username later if this part works
        # keys into resp are probably different for different oauth providers, unfortunately
        session['login'] = dict(oauth_token=(resp['access_token'], resp['refresh_token']))
    except TypeError as exc:
        flash('The login request was gracefully declined. (TypeError: %s)' % exc)
        return redirect(url_for('index'))
    except KeyError as exc:
        flash('There was a problem with the response dictionary. (KeyError: %s) %s' % (exc, resp))
        return redirect(url_for('index'))
    
    log.debug('oauth_authorized response %s', resp)
    
    # now get their username
    me = auth.get('people/me')
    if me.status == 200:
        session['login']['user'] = '{first_name} {last_name}'.format(**me.data)
        session['login']['email'] = me.data['email']
        session['login']['image'] = me.data['image']
    else:
        session['login']['user'] = 'Hacker Schooler'
    flash('You are logged in.')
    return redirect(request.args.get('next') or url_for('index'))

@app.route('/logout')
def logout():
    # the important bit here is to remove the login from the session
    flash('You have logged out.') if session.pop('login', None) \
        else flash('You aren\'t even logged in.')
    return redirect(url_for('index'))

## pages ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ## ##

@app.route('/')
def index():
    return render_template('base.html', login=get_login())
    
@app.route('/pairmatch')
@protected
def pairmatch(login=None):
    match_candidates = [p for p in hsapi.active_batch_members() if p['email'] != login['email']]
    match = choice(match_candidates)
    return render_template('match.html', login=login, match=match)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')
        
# eof
