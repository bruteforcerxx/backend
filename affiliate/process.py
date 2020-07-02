from django.contrib.auth.models import User
from coinbase.wallet.client import Client
from .models import Agent
from home.models import UsersData
from transactions_history.models import History
import string
import random


def get_agent_info(user):
    agent_data = Agent.objects.get(name=user)

    rank = agent_data.rank
    code = agent_data.referral_code
    earned = agent_data.total_earned
    p_down_lines = eval(agent_data.primary_down_lines)
    s_down_lines = eval(agent_data.total_primary_down_lines)
    t_pdl = agent_data.total_primary_down_lines
    t_sdl = agent_data.total_secondary_down_lines
    link = f'http://127.0.0.1:8000/home/register/{code}'

    context = {'rank': rank, 'code': code, 'earned': earned, 'p_down': p_down_lines,
               's_down': s_down_lines, 'link': link}
    print(context)
    return context


def get_amount(currency):
    key = "qllinMZsWKJxMbm1"
    secret = "O8166FUvpXgZk5XowalRE8cP0tVXRWkT"
    client = Client(key, secret)
    pair = f'{currency}-NGN'
    price = client.get_spot_price(currency_pair=pair)
    amount = float(price['amount'])
    amount = 1500.00/amount
    amount = float("{:.8f}".format(amount))
    print(amount)
    return amount


def get_payment(cu, user, amount, currency):
    username = User.objects.get(username=user)
    user = UsersData.objects.get(user=username)
    hist = History.objects.get(user=username)
    letters = string.ascii_lowercase
    identity = ''.join(random.choice(letters) for _ in range(30))

    param = {'to': 'affiliate registration', 'amount': amount, 'desc': 'affiliate registration fee',
             'currency': currency, 'platform': 'axemo', 'user': user, 'route': 'axemo', 'type': 'Debit',
             'status': 'success', 'resolved': True}
    if cu == 'BTC':
        bal = user.bitcoin_balance
        if bal < amount:
            return 'failed'
        bal -= amount
        user.bitcoin_balance = bal
        history = eval(hist.btc_history)
        history[identity] = param
        hist.btc_history = str(history)
    elif cu == 'ETH':
        bal = user.etherum_balance
        if bal < amount:
            return 'failed'
        bal -= amount
        user.etherum_balance = bal
        history = eval(hist.eth_history)
        history[identity] = param
        hist.eth_history = str(history)
    elif cu == 'LTC':
        bal = user.litecoin_balance
        if bal < amount:
            return 'failed'
        bal -= amount
        user.litecoin_balance = bal
        history = eval(hist.ltc_history)
        history[identity] = param
        hist.ltc_history = str(history)
    elif cu == 'BCH':
        bal = user.bitcoin_cash_balance
        if bal < amount:
            return 'failed'
        bal -= amount
        user.bitcoin_cash_balance = bal
        history = eval(hist.bch_history)
        history[identity] = param
        hist.bch_history = str(history)
    elif cu == 'NGN':
        bal = user.local_currency_balance
        if bal < amount:
            return 'failed'
        bal -= amount
        user.local_currency_balance = amount
        history = eval(hist.ngn_history)
        history[identity] = param
        hist.ngn_history = str(history)

    user.save()
    hist.save()
    return 'success'


def process_request(user, amount):
    agent = User.objects.get(username=user)
    get_ref = UsersData.objects.get(user=agent)
    referral = get_ref.referral
    p_ref = Agent.objects.filter(referral=referral)

    if len(p_ref) < 1:
        return
    p_ref = p_ref[0]
    rank = p_ref.rank
    bal = p_ref.total_earned
    dl = eval(p_ref.primary_down_lines)

    if rank == 'standard':
        bal += (50 / 100) * 1500
    elif rank == 'pro':
        bal += (75 / 100) * 1500
    elif rank == 'premium':
        bal += 1500

    p_ref.total_earned = bal
    p_ref.total_primary_down_lines += 1
    dl.append(user)
    p_ref.primary_down_lines = str(dl)

    p_ref.save()

    s_ref = User.objects.get(username=p_ref)
    s_ref = Agent.objects.filter(referral=s_ref)
    if len(s_ref) == 1:
        s_ref = s_ref[0]
        s_bal = s_ref.total_earned
        s_sdl = eval(s_ref.secondary_down_line)
        s_bal += (10 / 100) * amount
        s_ref.total_earned = s_bal
        s_ref.total_secondary_down_lines += 1
        s_sdl.append(user)
        s_ref.secondary_down_line = str(dl)
        s_ref.save()

    user = User.objects.get(username=user)
    reg_agent = Agent(user=user)
    reg_agent.save()


def transfer(user, amount):
    user_d = UsersData.objects.get(user=user)
    aff = Agent.objects.get(name=user)
    hist = History.objects.get(user=user)

    letters = string.ascii_lowercase
    identity = ''.join(random.choice(letters) for _ in range(30))

    param = {}

    if aff.total_earned < amount:
        return 'failed'

    aff.total_earned -= amount
    user_d.local_currency_balance += amount
    history = eval(hist.ngn_history)
    history[identity] = param
    hist.ngn_history = str(history)

    user_d.save()
    aff.save()
    hist.save()

    return 'success'


def pay_for_upgrade(user):
    agent = Agent.objects.get(referral=user)

    if agent.rank == 'standard':
        if agent.total_earned >= 3000:
            agent.total_earned -= 3000
            agent.rank = 'pro'
            return 'upgraded successfully'
        else:
            return 'insufficient balance'

    elif agent.rank == 'pro':
        if agent.total_earned >= 6000:
            agent.total_earned -= 6000
            agent.rank = 'premium'
            return 'upgraded successfully'
        else:
            return 'insufficient balance'
    agent.save()

