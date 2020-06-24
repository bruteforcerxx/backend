from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import status
from django.template import loader
from home.models import RegForm
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from home.models import UsersData
from .process import process_request, get_payment, get_agent_info
from .models import Agent
from transactions_history.models import History
from django.shortcuts import redirect
import time

# Create your views here.


@api_view(['GET'])
def info(request):
    try:
        if request.session['session_timeout'] > time.time():
            print(f"time left = {request.session['session_timeout'] - time.time()} seconds")
            request.session['session_timeout'] = time.time() + 600

            user = User.objects.get(username=request.user)
            agent = Agent.objects.filter(name=user)

            if len(agent) > 0:
                context = get_agent_info(user)
                page = 'agentpage.html'
                # template = loader.get_template(page)
                return Response(context, status=status.HTTP_200_OK)
                # return HttpResponse(template.render(context, request), status=status.HTTP_200_OK)
            else:
                page = 'agentreg.html'
                template = loader.get_template(page)
                return HttpResponse(template.render({'header': 'TESTING agent VIEW'}, request),
                                    status=status.HTTP_200_OK)
        else:
            logout(request)
            return redirect('login')

    except Exception as e:
        print(e)
        return redirect('login')


@api_view(['GET', 'POST'])
def payment_method(request):
    if request.method == 'GET':
        page = 'register.html'
        template = loader.get_template(page)
        context = {'currency': {'Bitcoin': f'{0.0000234}btc', 'Etherum': f'{0.001234}eth', 'Litecoin': f'{0.016633}ltc',
                                'Bitcoin cash': f'{0.02123}bch', 'Naira': f'{1500}NGN'}}
        return HttpResponse(template.render(context, request), status=status.HTTP_200_OK)


@api_view(['POST'])
def payment(request, currency):
    # amount = request.session['amount']
    username = 'flasker'
    password = '1111'
    try:
        if authenticate(username=username, password=password):
            print('AUTHENTICATED')
            # get_payment(currency, request.user, amount)
            # process_request(request.user, amount)

            # page = 'regcomp.html'
            # template = loader.get_template(page)
            return Response(currency, status=status.HTTP_200_OK)
            # return HttpResponse(template.render({'header': 'TESTING agent VIEW'}, request), status=status.HTTP_200_OK)

        else:
            return Response('something went wrong', status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print(e)
        logout(request)
        redirect('login')


def upgrade(request):
    from django.shortcuts import redirect
    user = User.objects.get(username=request.user)
    aff = Agent.objects.get(user=user)
    page = 'regcomp.html'
    template = loader.get_template(page)

    level = aff.rank
    dl = aff.primary_down_lines

    next = 'pro'
    if level == 'standard':
        next = 'pro'
    if level == 'pro':
        next = 'premium'

    if level == 'standard':
        if dl >= 10:
            return redirect(pay_upgrade, next)
    elif level == 'pro':
        if dl >= 30:
            return redirect(pay_upgrade, next)
    else:
        print(level)
        print('not ready')
        return HttpResponse(template.render({'header': 'TESTING agent VIEW'}, request), status=status.HTTP_200_OK)


def pay_upgrade(request, next):

    if request.method == 'GET':
        if next == 'pro':
            pass
        elif next == 'premium':
            pass
    if request.method == 'POST':
        fee = None
        if next == 'pro':
            fee = 2002.393
        if next == 'pro':
            fee = 6966.393


        #return HttpResponse(template.render({'header': 'TESTING agent VIEW'}, request), status=status.HTTP_200_OK)


def process_upgrade():
    currency = ''

    #get_payment(currency, request.user, amount)
    #pay_referral(currency, request.user, fee)
    #return HttpResponse(template.render({'header': 'TESTING agent VIEW'}, request), status=status.HTTP_200_OK)