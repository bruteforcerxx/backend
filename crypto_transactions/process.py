from coinbase.wallet.client import Client
from transactions_history.models import History
from django.contrib.auth.models import User
from home.models import UsersData
import string
import random
from .models import DebitTransaction, Address


# make transaction here
key = "qllinMZsWKJxMbm1"
secret = "O8166FUvpXgZk5XowalRE8cP0tVXRWkT"
btc_id ="98d51393-b7bf-5381-b727-21200c515708"


def get_address(user, cu):

    print(type(cu))
    client = Client(key, secret)
    address = client.create_address(btc_id)
    user = User.objects.get(username=user)
    address_saver = Address(user=user, address=address['address'], currency=cu)
    address_saver.save()
    return address['address']


def coinbase(param):

    print(f'data: {param}')
    try:
        tx = ['completed']
        # client = Client(key, secret)
        # tx = client.send_money(btc_id, to=param['to'], amount=param['amount], currency=param['currency'],
        # desc=param[desc])
        if 'completed' in tx:
            param['status'] = 'success'
            param['resolved'] = True
            currency = param['currency']
            user = User.objects.get(username=param['user'])
            user = UsersData.objects.get(user=user)
            print(f'{user}'*10)
            if currency == 'BTC':
                balance = float(user.bitcoin_balance)
                balance -= float(param['amount'])
                user.bitcoin_balance = balance
                print(f'{balance}' * 10)
            elif currency == 'ETH':
                balance = float(user.etherum_balance)
                balance -= float(param['amount'])
                user.etherum_balance = balance
                print(f'{balance}' * 10)
            elif currency == 'LTC':
                balance = float(user.litecoin_balance)
                balance -= float(param['amount'])
                user.litecoin_balance = balance
                print(f'{balance}' * 10)
            elif currency == 'BTC':
                balance = float(user.bitcoin_cash_balance)
                balance -= float(param['amount'])
                user.bitcoin_cash_balance = balance
                print(f'{balance}' * 10)
            print(f'***' * 10)
            user.save()
            print(f'***' * 10)
            save(param)
            print('success'*10)
            return 'success'
        else:
            return 'transaction failed'
    except IndexError as e:
        print('error'*10)
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
        sender = param['user']
        currency = param['currency']
        print(currency)
        if User.objects.get(email=receiver):
            user = User.objects.get(username=sender)
            user = UsersData.objects.get(user=user)
            if currency == 'BTC':
                balance = float(user.bitcoin_balance)
                print(balance)
                balance -= float(param['amount'])
                user.bitcoin_balance = balance
                print(user.bitcoin_balance)
            elif currency == 'ETH':
                balance = float(user.etherum_balance)
                print(balance)
                balance -= float(param['amount'])
                user.etherum_balance = balance
                print(user.etherum_balance)
            elif currency == 'LTC':
                balance = float(user.litecoin_balance)
                print(balance)
                balance -= float(param['amount'])
                user.litecoin_balance = balance
                print(user.litecoin_balance)
            elif currency == 'BCH':
                balance = float(user.bitcoin_cash_balance)
                print(balance)
                balance -= float(param['amount'])
                user.bitcoin_cash_balance = balance
                print(user.bitcoin_cash_balance)
            user.save()
            param['type'] = 'Transfer'
            param['status'] = 'success'
            param['resolved'] = True

            identity = save(param)
            print(identity*10)

            receiver = User.objects.get(email=receiver)
            r = UsersData.objects.get(user=receiver)
            hist = History.objects.get(user=receiver)

            if currency == 'BTC':
                balance = float(r.bitcoin_balance)
                print(balance)
                balance += float(param['amount'])
                r.bitcoin_balance = balance
                print(r.bitcoin_balance)
                history = eval(hist.btc_history)
                history[identity] = param
                hist.btc_history = str(history)
            elif currency == 'ETH':
                balance = float(r.etherum_balance)
                balance += float(param['amount'])
                r.etherum_balance = balance
                history = eval(hist.eth_history)
                history[identity] = param
                hist.eth_history = str(history)
            elif currency == 'LITE':
                balance = float(r.litecoin_balance)
                balance += float(param['amount'])
                r.litecoin_balance = balance
                history = eval(hist.ltc_history)
                history[identity] = param
                hist.ltc_history = str(history)
            elif currency == 'BCH':
                balance = float(r.bitcoin_cash_balance)
                balance += float(param['amount'])
                r.bitcoin_cash_balance = balance
                history = eval(hist.bch_history)
                history[identity] = param
                hist.bch_history = str(history)
            hist.save()
            r.save()
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
    cur = param['currency']

    letters = string.ascii_lowercase
    identity = ''.join(random.choice(letters) for _ in range(30))

    user = User.objects.get(username=username)
    hist = History.objects.get(user=user)

    print(cur)

    if cur == 'BTC':
        history = eval(hist.btc_history)
        history[identity] = param
        hist.btc_history = str(history)
    elif cur == 'ETH':
        history = eval(hist.eth_history)
        history[identity] = param
        hist.eth_history = str(history)
    elif cur == 'LTC':
        history = eval(hist.ltc_history)
        history[identity] = param
        hist.ltc_history = str(history)
    elif cur == 'BCH':
        history = eval(hist.bch_history)
        history[identity] = param
        hist.bch_history = str(history)

    hist.save()

    dec = param['desc']
    description = f'From: axemo \n sender: {user} \n description: {dec}'
    debit = DebitTransaction(user=user, username=username, tx_hash=identity, amount=param['amount'],
                             description=description, destination=param['to'],
                             status=param['status'], resolve=param['resolved'], route=param['route'])
    debit.save()
    print('transaction saved')
    return identity
