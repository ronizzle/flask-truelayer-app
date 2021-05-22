from flask import (
    Blueprint, redirect, render_template, url_for, request, session
)


import requests

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    login_url = link_builder()
    return render_template('auth/login.html', login_url=login_url)


@bp.route('/logout')
def logout():
    # destroy truelayer session here
    return redirect(url_for('index'))


@bp.route('/callback', methods=('GET', 'POST'))
def callback():
    connect_token(request.args['code'])
    return render_template('auth/success.html')


def link_builder():
    base_url = 'https://auth.truelayer-sandbox.com/'
    code = 'code'
    scope = 'info accounts balance cards transactions direct_debits standing_orders offline_access'
    redirect_uri = 'http://localhost:5000/auth/callback'
    providers = 'uk-ob-all uk-oauth-all uk-cs-mock'
    client_id = 'sandbox-rbernascodetest01-a16f09'

    url = base_url + '?response_type=' + code + '&client_id=' + client_id + '&scope=' + scope + '&redirect_uri=' + redirect_uri + '&providers=' + providers
    return url


def connect_token(code):
    base_url = 'https://auth.truelayer-sandbox.com/'
    url = base_url + 'connect/token'
    client_id = 'sandbox-rbernascodetest01-a16f09'
    client_secret = '7ba394ff-faa9-43dd-ac47-63c124708a19'
    redirect_uri = 'http://localhost:5000/auth/callback'
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

    if token_json['access_token']:
        session['refresh_token'] = token_json['refresh_token']
        session['access_token'] = token_json['access_token']
        return token_json
    else:
        return render_template('auth/error.html')
