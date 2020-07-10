from django.http import HttpResponse
from rest_framework import status
from django.template import loader
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import logout, login, authenticate
from home.models import UsersData
from .process import process_request, get_payment, get_agent_info, pay_for_upgrade, get_amount, transfer
from .models import Agent
from django.shortcuts import redirect
import time
import hashlib

# Create your views here.


@api_view(['GET'])
def info(request):
    print('*'*100)
    try:
        if request.session['session_timeout'] > time.time():
            print(f"time left = {request.session['session_timeout'] - time.time()} seconds")
            request.session['session_timeout'] = time.time() + 100000000000
            print('*' * 100)

            user = User.objects.get(username=request.user)
            agent = Agent.objects.filter(name=user)

            if len(agent) == 1:
                page = 'pages/affiliate.html'
                template = loader.get_template(page)
                context = get_agent_info(user)
                return Response(context)
                # return HttpResponse(template.render(context, request), status=status.HTTP_200_OK)

            else:
                context = {'message': 'not registered'}
                page = 'pages/affiliate_reg.html'
                template = loader.get_template(page)
                return HttpResponse(template.render(context, request), status=status.HTTP_200_OK)

        else:
            logout(request)
            return redirect('login')

    except IndexError as e:
        print(e)
        return redirect('login')


@api_view(['POST'])
def debit_user(request):
    pin = str(request.POST.get('pin', ''))
    currency = request.POST.get('currency', '')

    user = User.objects.get(username=request.user)
    user_d = UsersData.objects.get(user=user)

    # 9af15b336e6a9619928537df30b2e6a2376569fcf9d7e773eccede65606529a0
    if hashlib.sha256(pin.encode()).hexdigest() == str(user_d.pin):
        amount = get_amount(currency)

        if get_payment(currency, request.user, amount, currency) == 'success':
            process_request(request.user, amount)
            context = 'successful'
        else:
            context = 'insufficient funds'
        return Response(context, status=status.HTTP_200_OK)

    else:
        context = 'incorrect pin'
        return Response(context, status=status.HTTP_406_NOT_ACCEPTABLE)


@api_view(['POST', 'GET'])
def upgrade(request):
    user = User.objects.get(username=request.user)
    user_d = UsersData.objects.get(user=user)
    aff = Agent.objects.get(name=user)

    if request.method == 'GET':
        page = 'upgrade_agent.html'
        template = loader.get_template(page)
        lev = None
        if aff.rank == 'standard':
            lev = 'pro'
        elif aff.rank == 'pro':
            lev = 'premium'

        return HttpResponse(template.render({'message': f'upgrade to a {lev} agent'},
                                            request), status=status.HTTP_200_OK)
    if request.method == 'POST':
        pin = str(request.POST.get('pin', ''))

        # 9af15b336e6a9619928537df30b2e6a2376569fcf9d7e773eccede65606529a0
        if hashlib.sha256(pin.encode()).hexdigest() == str(user_d.pin):
            level = aff.rank
            dl = aff.primary_down_lines

            if level == 'standard':
                if len(eval(dl)) >= 10:
                    response = pay_for_upgrade(user)
                    return Response({response}, status=status.HTTP_200_OK)

                else:
                    return Response({'not ready. get at lease 10 primary down lines before you can upgrade '},
                                    status=status.HTTP_406_NOT_ACCEPTABLE)

            elif level == 'pro':
                if len(eval(dl)) >= 30:
                    response = pay_for_upgrade(user)
                    return Response({response}, status=status.HTTP_200_OK)

                else:
                    return Response({'not ready. get at lease 10 primary down lines before you can upgrade '},
                                    status=status.HTTP_406_NOT_ACCEPTABLE)

        else:
            context = 'incorrect pin'
            return Response(context, status=status.HTTP_406_NOT_ACCEPTABLE)


@api_view(['POST', 'GET'])
def withdraw(request):

    if request.method == 'GET':
        user = User.objects.get(username=request.user)
        aff = Agent.objects.get(name=user)

        if aff.total_earned >= 5000:
            page = 'withdraw.html'
            template = loader.get_template(page)
            context = {'method': 'Enter amount and provide your pin to proceed'}
            return HttpResponse(template.render(context, request), status=status.HTTP_200_OK)
        else:
            context = 'Insufficient balance, accumulate a total of 5000 before you can withdraw'
            return Response(context, status=status.HTTP_200_OK)

    if request.method == 'POST':
        pin = str(request.POST.get('pin', ''))
        amount = float(request.POST.get('amount', ''))

        user = User.objects.get(username=request.user)
        user_d = UsersData.objects.get(user=user)

        if hashlib.sha256(pin.encode()).hexdigest() == str(user_d.pin):
            pay = transfer(user, amount)
            if pay == 'success':
                context = 'Transfer successful'
                return Response(context, status=status.HTTP_200_OK)
            else:
                context = 'Transfer failed. Insufficient balance'
                return Response(context, status=status.HTTP_200_OK)


@api_view(['GET'])
def test(request):
    if request.method == 'GET':
        page = 'pages/adress.html'
        template = loader.get_template(page)
        context = {'method': 'choose payment method'}
        return HttpResponse(template.render(context, request), status=status.HTTP_200_OK)


