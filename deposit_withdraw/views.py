from django.shortcuts import render
from django.http import HttpResponse
from .models import BuyForm, SellForm, WithdrawForm, DepositForm
from rest_framework import status
from django.template import loader
from django.contrib.auth import logout
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from home.models import UsersData
from django.shortcuts import redirect
from .process import buy_crypto, sell_crypto, deposit_money, withdraw_money, load_history
import time
from transactions_history.models import History
import hashlib
from rave_python import Rave
# Create your views here.


@api_view(['GET'])
def naira_account(request):

    try:
        if request.session['session_timeout'] > time.time():
            print(f"time left = {request.session['session_timeout'] - time.time()} seconds")
            request.session['session_timeout'] = time.time() + 600

            history = load_history()
            user = User.objects.get(username=request.user)
            user = UsersData.objects.get(user=user)
            history = History.objects.get(user)
            naira_his = eval(history.ngn_history)

            naira_balance = user.local_balance

            page = 'naira.html'
            template = loader.get_template(page)

            return HttpResponse(template.render({'message': 'naira account'}, request),
                                status=status.HTTP_200_OK)

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
                form_model = BuyForm
                form = form_model(None)

                page = 'request.html'
                template = loader.get_template(page)

                currency = request.session['currency']

                message = f'complete details to send {currency}'
                return HttpResponse(template.render({'form': form, 'message': message}, request),
                                    status=status.HTTP_200_OK)

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
                form_model = SellForm
                form = form_model(None)

                page = 'request.html'
                template = loader.get_template(page)

                currency = request.session['currency']

                message = f'complete details to send {currency}'
                return HttpResponse(template.render({'form': form, 'message': message}, request),
                                    status=status.HTTP_200_OK)

            if request.method == 'POST':
                pass

        else:
            logout(request)
            return redirect('login')

    except Exception as e:
        print(e)
        logout(request)
        return redirect('login')


def deposit(request):
    try:
        if request.session['session_timeout'] > time.time():
            print(f"time left = {request.session['session_timeout'] - time.time()} seconds")
            request.session['session_timeout'] = time.time() + 600

            if request.method == 'GET':
                form_model = DepositForm
                form = form_model(None)

                page = 'request.html'
                template = loader.get_template(page)

                currency = request.session['currency']

                message = f'complete details to send {currency}'
                return HttpResponse(template.render({'form': form, 'message': message}, request),
                                    status=status.HTTP_200_OK)

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
                form_model = WithdrawForm
                form = form_model(None)

                page = 'request.html'
                template = loader.get_template(page)

                currency = request.session['currency']

                message = f'complete details to send {currency}'
                return HttpResponse(template.render({'form': form, 'message': message}, request),
                                    status=status.HTTP_200_OK)

            if request.method == 'POST':
                pass

        else:
            logout(request)
            return redirect('login')

    except Exception as e:
        print(e)
        logout(request)
        return redirect('login')

