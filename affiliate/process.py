from django.contrib.auth.models import User
from home.models import UsersData
from .models import Agent
from home.models import UsersData
from transactions_history.models import History
from django.contrib.auth import authenticate
import string
import random


def get_agent_info(user):
    agent = Agent.objects.get(name=user)
    rank = agent.rank
    link = agent.referral_link
    code = agent.referral_code
    p_dl = eval(agent.primary_down_lines)
    s_dl = eval(agent.secondary_down_lines)
    t_pdl = agent.total_primary_down_lines
    t_sdl = agent.total_secondary_down_lines
    earned = agent.total_earned
    info = {'rank': rank, 'link': link, 'code': code, 'pdl': p_dl, 'sdl': s_dl, 't_pdl': t_pdl, 't_sdl': t_sdl,
            'earned': earned}
    return info


def get_payment(cu, user, amount):
    usern = User.objects.get(username=user)
    user = UsersData.objects.get(user=usern)
    hist = History.objects.get(user=usern)
    letters = string.ascii_lowercase
    identity = ''.join(random.choice(letters) for _ in range(30))

    param = {}
    bal = 0
    if cu == 'BTC':
        bal = user.bitcoin_balance
        bal -= amount
        user.bitcoin_balance = bal
        history = eval(hist.btc_history)
        history[identity] = param
        hist.btc_history = str(history)
    elif cu == 'ETH':
        bal = user.etherum_balance
        bal -= amount
        user.etherum_balance = bal
        history = eval(hist.eth_history)
        history[identity] = param
        hist.eth_history = str(history)
    elif cu == 'LTC':
        bal = user.litecoin_balance
        bal -= amount
        user.litecoin_balance = bal
        history = eval(hist.ltc_history)
        history[identity] = param
        hist.ltc_history = str(history)
    elif cu == 'BCH':
        bal = user.bitcoin_cash_balance
        bal -= amount
        user.bitcoin_cash_balance = bal
        history = eval(hist.bch_history)
        history[identity] = param
        hist.bch_history = str(history)
    elif cu == 'NGN':
        bal = user.local_currency_balance
        bal -= amount
        user.local_currency_balance = amount
        history = eval(hist.ngn_history)
        history[identity] = param
        hist.ngn_history = str(history)

    user.save()
    hist.save()


def process_request(user, amount):
    agent = User.objects.get(username=user)
    get_ref = UsersData.objects.get(user=agent)
    referral = get_ref.referral
    p_ref = Agent.objects.get(referral=referral)
    s_ref = User.objects.get(username=p_ref)
    get_s_ref = UsersData.objects.get(user=s_ref)
    s_ref = Agent.objects.get(referral=get_s_ref)

    rank = p_ref.rank
    bal = p_ref.total_earned
    dl = eval(p_ref.primary_down_lines)
    s_bal = s_ref.total_earned
    s_sdl = eval(s_ref.secondary_down_line)

    if rank == 'standard':
        bal += (50 / 100) * amount
    elif rank == 'pro':
        bal += (75 / 100) * amount
    elif rank == 'premium':
        bal += amount
        s_bal += (10 / 100) * amount

    s_bal += (10 / 100) * amount
    p_ref.total_earned = bal
    s_ref.total_earned = s_bal
    s_ref.total_primary_down_lines += 1
    s_ref.total_secondary_down_lines += 1
    dl.append(user)
    s_sdl.append(user)
    p_ref.primary_down_lines = str(dl)
    s_ref.secondary_down_line = str(dl)

    p_ref.save()
    s_ref.save()

    user = authenticate(username=username, password=password)
    user = User.objects.get(username=user)
    reg_agent = Agent(user=user)
    reg_agent.save()


def pay_referral(user, amount):
    agent = User.objects.get(username=user)
    get_ref = UsersData.objects.get(user=agent)
    referral = get_ref.referral
    p_ref = Agent.objects.get(referral=referral)
    s_ref = User.objects.get(username=p_ref)
    get_s_ref = UsersData.objects.get(user=s_ref)
    s_ref = Agent.objects.get(referral=get_s_ref)

    rank = p_ref.rank
    bal = p_ref.total_earned
    s_bal = s_ref.total_earned

    if rank == 'standard':
        bal += (50 / 100) * amount
    elif rank == 'pro':
        bal += (75 / 100) * amount
    elif rank == 'premium':
        bal += amount
        s_bal += (10 / 100) * amount

    s_bal += (10 / 100) * amount
    p_ref.total_earned = bal
    s_ref.total_earned = s_bal

    p_ref.save()
    s_ref.save()



