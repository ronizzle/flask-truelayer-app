from flask import (
    Blueprint, redirect, render_template, url_for, request, session
)

import requests
from dotenv import dotenv_values

config = dotenv_values()

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if 'access_token' in session:
        return redirect('/home/dashboard')

    login_url = link_builder()
    return render_template('auth/login.html', login_url=login_url)


@bp.route('/logout')
def logout():
    session.pop('refresh_token', None)
    session.pop('access_token', None)
    return redirect('/auth/login')


@bp.route('/callback', methods=('GET', 'POST'))
def callback():
    token_json = connect_token(request.args['code'])
    return '<a href="/home/dashboard">Successfully logged in!. Click here to take you to your dashboard.</a>'
    # return render_template('auth/success.html')


def link_builder():
    base_url = config['TRUELAYER_AUTH_URL']
    code = config['TRUELAYER_CODE']
    scope = config['TRUELAYER_SCOPE']
    redirect_uri = config['TRUELAYER_REDIRECT_URI']
    providers = config['TRUELAYER_PROVIDERS']
    client_id = config['TRUELAYER_CLIENT_ID']

    url = base_url + '?response_type=' + code + '&client_id=' + client_id + '&scope=' + scope + '&redirect_uri=' + redirect_uri + '&providers=' + providers
    return url


def connect_token(code):
    base_url = config['TRUELAYER_AUTH_URL']
    url = base_url + 'connect/token'
    client_id = config['TRUELAYER_CLIENT_ID']
    client_secret = config['TRUELAYER_CLIENT_SECRET']
    redirect_uri = config['TRUELAYER_REDIRECT_URI']
    post_data = {
        'grant_type': 'authorization_code',
        'client_id': client_id,
        'client_secret': client_secret,
        'redirect_uri': redirect_uri,
        'code': code
    }

    client_auth = requests.auth.HTTPBasicAuth(client_id, client_secret)
    r = requests.post(url, auth=client_auth, data=post_data)
    token_json = r.json()
    session['refresh_token'] = token_json['refresh_token']
    session['access_token'] = token_json['access_token']
    return token_json
