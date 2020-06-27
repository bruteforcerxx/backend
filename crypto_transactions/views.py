from django.http import HttpResponse
from .models import TransferForm
from rest_framework import status
from django.template import loader
from .process import coinbase, luno, local, get_address
from django.contrib.auth import logout
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from home.models import UsersData
from django.shortcuts import redirect
import time
import hashlib

# Create your views here.


@api_view(['GET', 'POST'])
def crypto(request, currency):
    try:
        if request.session['session_timeout'] > time.time():
            print(f"time left = {request.session['session_timeout'] - time.time()} seconds")
            request.session['session_timeout'] = time.time() + 600

            page = 'selection.html'
            template = loader.get_template(page)

            request.session['currency'] = currency
            context = {'message': f'Select an action for {currency.capitalize()}', 'currency': currency}
            return HttpResponse(template.render(context, request), status=status.HTTP_200_OK)

        else:
            logout(request)
            return redirect('login')

    except Exception as e:
        print(e)
        logout(request)
        return redirect('login')


@api_view(['GET'])
def receive(request):
    try:
        if request.session['session_timeout'] > time.time():
            print(f"time left = {request.session['session_timeout'] - time.time()} seconds")
            request.session['session_timeout'] = time.time() + 600

            currency = request.session['currency']

            page = 'address.html'
            template = loader.get_template(page)

            context = {'address': get_address(request.user, currency)}
            return HttpResponse(template.render(context, request), status=status.HTTP_200_OK)

        else:
            logout(request)
            return redirect('login')

    except Exception as e:
        print(e)
        logout(request)
        return redirect('login')


@api_view(['GET', 'POST'])
def btc_select_platform(request):
    try:
        if request.session['session_timeout'] > time.time():
            print(f"time left = {request.session['session_timeout'] - time.time()} seconds")
            request.session['session_timeout'] = time.time() + 600

            if request.method == 'GET':
                page = 'btc_platforms.html'
                template = loader.get_template(page)

                return HttpResponse(template.render({'message': 'select a btc platform'}, request),
                                    status=status.HTTP_200_OK)

            if request.method == 'POST':
                request.session['btc_platform'] = request.POST.get('platform', '')
                return redirect(send)

        else:
            logout(request)
            return redirect('login')

    except Exception as e:
        print(e)
        logout(request)
        return redirect('login')


@api_view(['POST', 'GET'])
def select_other_platform(request, currency):
    try:
        if request.session['session_timeout'] > time.time():
            print(f"time left = {request.session['session_timeout'] - time.time()} seconds")
            request.session['session_timeout'] = time.time() + 600

            if request.method == 'GET':
                page = 'other_platforms.html'
                template = loader.get_template(page)

                currency = request.session['currency']

                return HttpResponse(template.render({'currency': currency}, request),
                                    status=status.HTTP_200_OK)

            if request.method == 'POST':
                request.session['btc_platform'] = request.POST.get('platform', '')
                return redirect(send)

        else:
            logout(request)
            return redirect('login')

    except Exception as e:
        print(e)
        logout(request)
        return redirect('login')


@api_view(['GET'])
def send(request):
    try:
        if request.session['session_timeout'] > time.time():
            print(f"time left = {request.session['session_timeout'] - time.time()} seconds")
            request.session['session_timeout'] = time.time() + 600

            form_model = TransferForm
            form = form_model(None)

            page = 'request.html'
            template = loader.get_template(page)

            currency = request.session['currency']

            message = f'complete details to send {currency}'
            return HttpResponse(template.render({'form': form, 'message': message}, request), status=status.HTTP_200_OK)

        else:
            logout(request)
            return redirect('login')

    except Exception as e:
        print(e)
        logout(request)
        return redirect('login')


@api_view(['POST', 'GET'])
def check(request):
    try:
        form = TransferForm(request.POST)
        page = 'confirm.html'
        template = loader.get_template(page)

        if request.method == 'POST':
            try:
                if request.session['session_timeout'] > time.time():
                    print(f"time left = {request.session['session_timeout'] - time.time()} seconds")
                    request.session['session_timeout'] = time.time() + 600

                    pin = '0000'
                    user = User.objects.get(username=request.user)
                    user_d = UsersData.objects.get(user=user)

                    print(hashlib.sha256(pin.encode()).hexdigest())
                    print(str(user_d.pin))

                    if hashlib.sha256(pin.encode()).hexdigest() == str(user_d.pin):
                        if form.is_valid():
                            print('FORM IS VALID')

                            to = form.cleaned_data['destination']
                            amount = float(form.cleaned_data['amount'])
                            desc = form.cleaned_data['description']
                            currency = request.session['currency']

                            context = {'to': to, 'amount': amount, 'desc': desc, 'currency': currency,
                                       'user': str(request.user)}
                            request.session['data'] = context
                            print(context)

                            return HttpResponse(template.render(context, request), status=status.HTTP_200_OK)

                        else:
                            context = {'form validation error': form.errors, 'data': request.POST}
                            return Response(context, status=status.HTTP_406_NOT_ACCEPTABLE)

                    else:
                        context = {'incorrect pin'}
                        return Response(context, status=status.HTTP_406_NOT_ACCEPTABLE)

                else:
                    logout(request)
                    return redirect('login')

            except Exception as e:
                print(e)
                logout(request)
                return redirect('login')

        if request.method == 'GET':
            params = request.session['data']
            platform = str(request.session['btc_platform'])

            currency = params['currency']
            user = params['user']
            amount = params['amount']
            params['route'] = platform

            if User.objects.get(username=user):
                user = User.objects.get(username=user)
                user = UsersData.objects.get(user=user)
                balance = 0.00

                if currency == 'BITCOIN':
                    balance = float(user.bitcoin_balance)
                    params['currency'] = 'BTC'

                elif currency == 'ETHERUM':
                    balance = float(user.etherum_balance)
                    params['currency'] = 'ETH'

                elif currency == 'LITECOIN':
                    balance = float(user.litecoin_balance)
                    params['currency'] = 'LTC'

                elif currency == 'BITCOINCASH':
                    balance = float(user.bitcoin_cash_balance)
                    params['currency'] = 'BCH'

                if balance >= float(amount):
                    response = 'request not resolved'

                    print(currency * 10)
                    if currency == 'BITCOIN':
                        params['route'] = platform

                        if platform == 'blockchain':
                            response = coinbase(params)

                        elif platform == 'coinbase':
                            response = coinbase(params)

                        elif platform == 'luno':
                            response = luno(params)

                        elif platform == 'axemo':
                            response = local(params)

                    else:
                        params['route'] = platform

                        if platform == 'blockchain':
                            response = coinbase(params)

                        elif platform == 'axemo':
                            response = local(params)

                    page = 'processed.html'
                    template = loader.get_template(page)

                    if response == 'success':
                        receiver = params['to']
                        context = {'status': 'success', 'detail': f'user: {user} sent {amount}Btc to  {receiver}.'}
                        return Response(context, status=status.HTTP_200_OK)
                        # return HttpResponse(template.render(context, request), status=status.HTTP_200_OK)

                    else:
                        return Response(response, status=status.HTTP_409_CONFLICT)

                else:
                    context = {'message': 'insufficient balance', 'user': str(user.user),
                               'user_balance': f'{balance}BTC', 'requested amount': f'{amount}BTC'}
                    return Response(context, status=status.HTTP_406_NOT_ACCEPTABLE)

            else:
                context = {'message': f'user: {user} does not exist'}
                return Response(context, status=status.HTTP_406_NOT_ACCEPTABLE)

        else:
            page = 'request.html'
            template = loader.get_template(page)
            return Response('something went wrong', status=status.HTTP_400_BAD_REQUEST)

            # return HttpResponse(template.render({'message': 'invalid request'}, request),
            # status=status.HTTP_406_NOT_ACCEPTABLE)

    except Exception as e:
        error = {'error': e}
        return Response(error, status=status.HTTP_400_BAD_REQUEST)


