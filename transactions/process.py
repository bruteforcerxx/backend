from coinbase.wallet.client import Client
from transactions.models import History
import json
import string
import random
from .models import DebitTransaction

# make transaction here
key = "qllinMZsWKJxMbm1"
secret = "O8166FUvpXgZk5XowalRE8cP0tVXRWkT"
id ="98d51393-b7bf-5381-b727-21200c515708"


def get_address(user):
    return 'address'


def coinbase(param):
    try:
        tx = ['completed']
        # client = Client(key, secret)
        # tx = client.send_money(id, to=param[2][0], amount=param[2][1], currency='BTC', desc=param[2][3])
        if 'completed' in tx:
            param['status'] = 'success'
            save(param)
            return 'success'
    except Exception as e:
        print(e)
        coinbase(param)


def luno(param):
    try:
        param['status'] = 'pending'
        save(param)
        return 'success'
    except Exception as e:
        print(e)


def local(param):
    try:
        # get sender and reciever and make transaction
        save(param)
        param['status'] = 'pending'
        return 'success'
    except Exception as e:
        print(e)


def save(param):
    hist = History.objects.filter(user=param['user'])[0]
    decoder = json.decoder.JSONDecoder()
    history = decoder.decode(hist.history)
    letters = string.ascii_lowercase
    identity = ''.join(random.choice(letters) for _ in range(30))
    history[identity] = param
    hist.history = json.dumps(history)
    hist.save()
    debit = DebitTransaction(user=param['user'], tx_hash=identity, amount=param['amount'],
                             platform=param['platform'], description=param['desc'], destination=param['to'],
                             status=param['status'])
    debit.save()
    print('transaction saved')
