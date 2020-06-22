from coinbase.wallet.client import Client
from transactions_history.models import History
from django.contrib.auth.models import User
from home.models import UsersData
import json
import string
import random
from .models import DebitTransaction
from rest_framework.response import Response
from rest_framework import status

# make transaction here
key = "qllinMZsWKJxMbm1"
secret = "O8166FUvpXgZk5XowalRE8cP0tVXRWkT"
id ="98d51393-b7bf-5381-b727-21200c515708"


def get_address(user):
    return 'address'


def coinbase(param):

    print(f'data: {param}')
    try:
        tx = ['completed']
        # client = Client(key, secret)
        # tx = client.send_money(id, to=param['to'], amount=param['amount], currency='BTC', desc=param[desc])
        if 'completed' in tx:
            param['status'] = 'success'
            param['resolved'] = True
            user = User.objects.get(username=param['user'])
            user = UsersData.objects.get(user=user)
            balance = float(user.bitcoin_balance)
            balance -= float(param['amount'])
            user.bitcoin_balance = balance
            user.save()
            save(param)
            return 'success'
        else:
            return 'transaction failed'
    except Exception as e:
        return str(e)


def luno(param):
    try:
        user = User.objects.get(username=param['user'])
        user = UsersData.objects.get(user=user)
        balance = float(user.bitcoin_balance)
        balance -= float(param['amount'])
        user.bitcoin_balance = balance
        user.save()

        param['status'] = 'pending'
        param['resolved'] = False
        save(param)
        return 'success'
    except Exception as e:
        return str(e)


def local(param):
    try:
        receiver = param['to']
        param['type'] = 'Credit'
        sender = param['user']
        if User.objects.get(email=receiver):
            user = User.objects.get(username=sender)
            user = UsersData.objects.get(user=user)
            balance = float(user.bitcoin_balance)
            balance -= float(param['amount'])
            user.bitcoin_balance = balance
            print('*'*100)

            receiver = User.objects.get(email=receiver)
            receiver_data = UsersData.objects.get(user=receiver)
            balance = float(receiver_data.bitcoin_balance)
            print(balance, receiver)
            balance += float(param['amount'])
            receiver_data.bitcoin_balance = balance
            print(balance, receiver)
            user.save()
            receiver_data.save()

            hist = History.objects.get(user=receiver)
            decoder = json.decoder.JSONDecoder()
            history = decoder.decode(hist.history)
            letters = string.ascii_lowercase
            identity = ''.join(random.choice(letters) for _ in range(30))
            history[identity] = param
            hist.history = json.dumps(history)

            hist.save()
            param['status'] = 'success'
            param['resolved'] = True
            save(param)
            return 'success'
        else:
            return f'User: {receiver} does not exist'
    except Exception as e:
        if str(e) == "User matching query does not exist.":
            return {'error': 'Invalid receivers address.',
                    'message': 'please cross-check address and try again'}
        else:
            return str(e)


def save(param):
    username = param['user']
    param['type'] = 'Debit'

    user = User.objects.get(username=username)
    hist = History.objects.get(user=user)

    decoder = json.decoder.JSONDecoder()
    history = decoder.decode(hist.history)
    letters = string.ascii_lowercase
    identity = ''.join(random.choice(letters) for _ in range(30))
    history[identity] = param
    hist.history = json.dumps(history)
    hist.save()
    debit = DebitTransaction(user=user, username=username, tx_hash=identity, amount=param['amount'],
                             platform=param['platform'], description=param['desc'], destination=param['to'],
                             status=param['status'], resolve=param['resolved'])
    debit.save()
    print('transaction saved')
