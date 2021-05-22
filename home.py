from flask import (
    Blueprint, redirect, render_template, url_for, request, session
)


import requests

bp = Blueprint('home', __name__, url_prefix='/home')


@bp.route('/dashboard')
def dashboard():
    accounts = get_accounts()
    #return accounts
    return render_template('home/dashboard.html', accounts=accounts)


@bp.route('/accounts/<string:id>')
def account(id):
    account = get_account_all_details(id)
    #return session['access_token']
    #return account
    return render_template('home/account.html', account=account)


def get_accounts():

    base_url = 'https://api.truelayer-sandbox.com/'
    url = base_url + 'data/v1/accounts'

    headers = {"Authorization": f"Bearer {session['access_token']}"}
    r = requests.get(url, headers=headers)

    r.raise_for_status()
    body = r.json()

    return body


def get_account_all_details(account_id):
    account = get_account(account_id)
    account['balance'] = get_account_balance(account_id)
    account['transactions'] = get_account_transactions(account_id)
    return account


def get_account(account_id):

    base_url = 'https://api.truelayer-sandbox.com/'
    url = base_url + 'data/v1/accounts/' + account_id

    headers = {"Authorization": f"Bearer {session['access_token']}"}
    r = requests.get(url, headers=headers)

    r.raise_for_status()
    body = r.json()

    return body['results'][0]


def get_account_balance(account_id):

    base_url = 'https://api.truelayer-sandbox.com/'
    url = base_url + 'data/v1/accounts/' + account_id + '/balance'

    headers = {"Authorization": f"Bearer {session['access_token']}"}
    r = requests.get(url, headers=headers)

    r.raise_for_status()
    body = r.json()

    return body


def get_account_transactions(account_id):

    base_url = 'https://api.truelayer-sandbox.com/'
    url = base_url + 'data/v1/accounts/' + account_id + '/transactions'

    headers = {"Authorization": f"Bearer {session['access_token']}"}
    r = requests.get(url, headers=headers)

    r.raise_for_status()
    body = r.json()

    return body

