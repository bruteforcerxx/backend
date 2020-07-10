from django.shortcuts import render
from django.http import HttpResponse
# from .models import
from rest_framework import status
from django.template import loader
from django.contrib.auth import logout
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from home.models import UsersData
from django.shortcuts import redirect
from .process import buy_crypto, sell_crypto, deposit_money_cad, withdraw_money,\
    load_history, deposit_money_account, otp_validation, url_auth, bal_converter
import time
from transactions_history.models import History
from threading import Thread
import hashlib
from rave_python import Rave
import json
# Create your views here.


@api_view(['GET'])
def naira_account(request):
    try:
        request.session['session_timeout'] = time.time() + 60000000
        if request.session['session_timeout'] > time.time():
            print(f"time left = {request.session['session_timeout'] - time.time()} seconds")
            request.session['session_timeout'] = time.time() + 60000000

            page = 'pages/naira.html'
            template = loader.get_template(page)

            logged_user = User.objects.get(username=request.user)

            user = UsersData.objects.get(user=logged_user)

            ngn = str(user.local_currency_balance)
            bal = bal_converter(ngn)
            print(bal)

            hist = History.objects.get(user=logged_user)

            history = []
            for h, i in eval(hist.ngn_history).items():
                history.append(i)

            history.reverse()
            message = [None, None]
            try:
                message = request.session['auth_message']
                print(message)
                request.session['auth_message'] = [None, None]
            except Exception as e:
                print(e)
                pass

            context = {'local': bal, 'currency': 'Naira', 'history': history, 'symbol': 'NGN', 'status': message[0],
                       'message': message[1]}
            return HttpResponse(template.render(context, request), status=status.HTTP_200_OK)

        else:
            logout(request)
            return redirect('login')

    except Exception as e:
        print(e)
        logout(request)
        return redirect('login')



@api_view(['GET'])
def deposit_card(request):
    try:
        if request.session['session_timeout'] > time.time():
            print(f"time left = {request.session['session_timeout'] - time.time()} seconds")
            request.session['session_timeout'] = time.time() + 600000

            user = User.objects.get(username=request.user)

            payload = request.session['payload']

            name = payload.get('card-name', '')
            name = name.split()
            if len(name) < 2:
                name.append('unknown')
                name.append('unknown')

            amount = payload.get('card-amount', '')

            pin = f"{payload.get('card-pin', '')}"

            print(payload)
            payload = {
                "cardno": f"{payload.get('card-number', '')}",
                "cvv": f"{payload.get('card-cvv', '')}",
                "expirymonth": f"{payload.get('card-date', '')[5:]}",
                "expiryyear": f"{payload['card-date'][:4]}",
                "amount": f"{payload.get('card-amount', '')}",
                "email": f"{user.email}",
                "phonenumber": '08108105750',
                "firstname": f"{name[0]}",
                "lastname": f"{name[1]}",
                "IP": "355426087298442",
                "redirect_url": "http://192.168.43.83:8000/fiat/validate-3Dsecure/",
            }
            print(payload)

            request.session['payload'] = 'fuck you!!'

            print('PASS')
            response = deposit_money_cad(payload, pin)
            if response[2] == 'otp required':
                print(response, '*'*10)
                request.session['otp-validate'] = [response[0], response[1], amount]

                page = 'pages/confirm_deposit.html'
                template = loader.get_template(page)

                return HttpResponse(template.render({'message': None}, request), status=status.HTTP_200_OK)

            if response[2] == '3D secure validation':
                request.session['url-validate'] = [response[0], amount]

                return redirect(response[1])
            else:
                print(response)
                if len(response) < 43:
                    request.session['auth_message'] = ['failed', 'Pin and cvv required']
                else:
                    request.session['auth_message'] = ['failed', response[43:]]
                return redirect(naira_account)

        else:
            pass
            logout(request)
            return redirect('login')

    except Exception as e:
        print(e)
        request.session['auth_message'] = ['failed', e[43:]]
        return redirect(naira_account)


@api_view(['POST'])
def otp_validate(request):

    try:
        if request.session['session_timeout'] > time.time():
            print(f"time left = {request.session['session_timeout'] - time.time()} seconds")
            request.session['session_timeout'] = time.time() + 600

            print(request.POST)
            otp = request.POST.get('otp', '')

            resp = request.session['otp-validate']
            response = otp_validation(resp, otp, request.user)

            if response == 'success':
                print('success')
                return redirect(naira_account)

            else:
                return Response(str(response), status=status.HTTP_401_UNAUTHORIZED)

        else:
            pass
            # logout(request)
            # return redirect('login')

    except Exception as e:
        print(e)
        request.session['auth_message'] = ['failed', e[43:]]
        return redirect(naira_account)


@api_view(['GET'])
def url_validate(request):
    response = request.GET['response']

    data = request.session['url-validate']

    stat = url_auth(data, response, request.user)

    if stat == 'success':
        request.session['auth_message'] = ['success', f'your deposit of NGN {data[1]} was successful!']
    else:
        request.session['auth_message'] = ['failed', f'your deposit of NGN {data[1]} failed']

    return redirect(naira_account)


@api_view(['POST'])
def res(request, section):
    try:
        if request.session['session_timeout'] > time.time():
            print(f"time left = {request.session['session_timeout'] - time.time()} seconds")
            request.session['session_timeout'] = time.time() + 600

            x = request.POST
            request.session['method'] = section
            request.session['payload'] = x
            print(section*100)

            return redirect(process)

        else:
            pass
            # logout(request)
            # return redirect('login')

    except Exception as e:
        print(e)
        # logout(request)
        # return redirect('login')


@api_view(['GET'])
def process(request):
    print('*'*100)

    try:
        if request.session['session_timeout'] > time.time():
            print(f"time left = {request.session['session_timeout'] - time.time()} seconds")
            request.session['session_timeout'] = time.time() + 600

            section = request.session['method']
            if section == 'naira-card-deposit':
                return redirect(deposit_card)

            if section == 'naira-account-deposit':
                x = {'account-amount': ['2222'], 'account-pin': ['2222']}

            if section == 'bank-account-transfer':
                x = {'bank-tf-amount': ['2222'], 'bank-tf-acc-num': ['2222222222'], 'bank-tf-password': ['2222']}

            if section == 'axemo-account-transfer':
                x = {'axemo-tf-amount': ['1111'], 'axemo-tf-account': ['sdfffffss'], 'account': ['2222']}

            if section == 'naira-withdraw':
                x = {'withdraw-amount': ['1111'], 'withdraw-pin': ['1111']}

            if section == 'buy-crypto':
                pass
            if section == 'sell-crypto':
                pass

        else:
            logout(request)
            return redirect('login')

    except Exception as e:
        print(e)
        logout(request)
        return redirect('login')


def buy(request):
    try:
        if request.session['session_timeout'] > time.time():
            print(f"time left = {request.session['session_timeout'] - time.time()} seconds")
            request.session['session_timeout'] = time.time() + 600

            if request.method == 'GET':
                pass
            if request.method == 'POST':
                pass

        else:
            logout(request)
            return redirect('login')

    except Exception as e:
        print(e)
        logout(request)
        return redirect('login')


def sell(request):
    try:
        if request.session['session_timeout'] > time.time():
            print(f"time left = {request.session['session_timeout'] - time.time()} seconds")
            request.session['session_timeout'] = time.time() + 600

            if request.method == 'GET':
                pass
            if request.method == 'POST':
                pass

        else:
            logout(request)
            return redirect('login')

    except Exception as e:
        print(e)
        logout(request)
        return redirect('login')





def withdraw(request):
    try:
        if request.session['session_timeout'] > time.time():
            print(f"time left = {request.session['session_timeout'] - time.time()} seconds")
            request.session['session_timeout'] = time.time() + 600

            if request.method == 'GET':

                page = 'request.html'
                template = loader.get_template(page)

                currency = request.session['currency']

                message = f'complete details to send {currency}'
               #  return HttpResponse(template.render({'form': form, 'message': message}, request),
                                  #   status=status.HTTP_200_OK)

            if request.method == 'POST':
                pass

        else:
            logout(request)
            return redirect('login')

    except Exception as e:
        print(e)
        logout(request)
        return redirect('login')

