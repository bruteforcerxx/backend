import requests
import time
import json
from decimal import Decimal
from coinbase.wallet.client import Client
from crypto_transactions.models import DebitTransaction
from transactions_history.models import History
from django.contrib.auth.models import User

balance_url = 'https://api.mybitx.com/api/1/balance'
address_url = 'https://api.mybitx.com/api/1/funding_address'
luno_send_url = 'https://api.mybitx.com/api/1/send'
key_id = 'k3ane3gbrr2pb'
secret_key = 'DADw2gjYH_dl9Kg6mLIMck8dqTSdfugJs9PYqYOdTXU'
associated_luno_email = 'olumichael2015@outlook.com'
coinbase_key = 'qllinMZsWKJxMbm1'
coinbase_secret = 'O8166FUvpXgZk5XowalRE8cP0tVXRWkT'
coinbase_id ="98d51393-b7bf-5381-b727-21200c515708"


def luno_sender():
    pending_luno_txs = DebitTransaction.objects.filter(platform='luno', status='pending', type='debit', resolve=False)
    total_amount = 0

    if len(pending_luno_txs) > 0:
        for p in pending_luno_txs:
            total_amount += p.amount

        print('total pending amount:', total_amount)
        payload = {'asset': 'XBT'}
        r = requests.get(balance_url, params=payload)
        rs = requests.get(r.url, auth=(key_id, secret_key)).json()

        luno_total_balance = rs['balance'][0]['balance']
        luno_reserve_balance = rs['balance'][0]['reserved']
        luno_balance = float(luno_total_balance) - float(luno_reserve_balance)
        print('available luno balance:', luno_balance)

        if float(luno_balance) < total_amount:
            r = requests.get(address_url, params=payload)
            rs = requests.get(r.url, auth=(key_id, secret_key)).json()
            luno_address = rs['address']
            print('luno address generated:', luno_address)

            print(f'requesting {total_amount} from coinbase...')
            client = Client(coinbase_key, coinbase_secret, api_version='YYYY-MM-DD')
            primary_account = client.get_primary_account()

            try:
                # primary_account.send_money(to=luno_address, amount=float(total_amount), currency='BTC')
                print('Balance sent!')
                print('waiting for credit..')
            except Exception as e:
                print(str(e))

            luno_balance = Decimal(luno_balance)
            while luno_balance < total_amount:
                time.sleep(3)  # 15 minutes
                payload = {'asset': 'XBT'}
                r = requests.get(balance_url, params=payload)
                rs = requests.get(r.url, auth=(key_id, secret_key)).json()

                print('checking balance...')
                luno_total_balance = rs['balance'][0]['balance']
                luno_reserve_balance = rs['balance'][0]['reserved']
                luno_balance = float(luno_total_balance) - float(luno_reserve_balance)
                print('balance:', luno_balance)
        else:
            pass

        print('Balance is sufficient.')
        print('initiating bulk transfers...')
        for p in pending_luno_txs:
            payload = {'amount': p.amount, 'currency': 'XBT', 'address': p.destination, 'description': p.description}
            r = requests.get(luno_send_url, params=payload)
            print(f'sending request to luno {p.destination}...')
            rs = requests.post(r.url, auth=(key_id, secret_key)).json()

            if 'success' in rs:
                p.status = 'success'
                p.resolved = True
                p.save()

                user = User.objects.get(username=p.username)
                hist = History.objects.get(user=user)

                decoder = json.decoder.JSONDecoder()
                history = decoder.decode(hist.history)
                for i, r in history.items():
                    if i == p.tx_hash:
                        r['resolved'] = True
                        r['status'] = 'success'

                hist.history = json.dumps(history)
                hist.save()

                print(f'sent {p.amount} to {p.destination} successfully.')
            else:
                print(f'error encountered while trying to send {p.amount} to {p.destination} ')
                p.resolved = True
                p.save()
    else:
        print('No pending and un-resolved luno transactions.')
