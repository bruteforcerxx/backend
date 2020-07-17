from django.http import HttpResponse
from rest_framework import status
from django.template import loader
from .models import RegForm
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import UsersData
from transactions_history.models import History
from django.shortcuts import redirect
import time
from .process import bal_converter


# Create your views here.


@api_view(['GET'])
def home_page(request):
    page = 'landing.html'
    template = loader.get_template(page)
    logout(request)
    return HttpResponse(template.render({'header': 'TESTING ABOUT VIEW'}, request), status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
def login_user(request):
    if request.method == 'GET':
        page = 'pages/login.html'
        template = loader.get_template(page)
        logout(request)
        return HttpResponse(template.render({'message': ''}, request), status=status.HTTP_200_OK)

    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        user = authenticate(username=username, password=password)
        if authenticate(username=username, password=password):
            login(request, user)

            request.session['current_user'] = username
            request.session['user_password'] = password

            request.session.set_expiry(0)
            request.session['session_timeout'] = time.time() + 100000
            print(request.session['session_timeout'])

            return redirect(dash)

        else:
            error = {'error': 'non-existent  account',
                     'message': 'the credentials you provided are not valid. Please cross-check and try again or '
                                'register a new account if you do not have an account'}
            return Response(error, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET', 'POST'])
def dash(request):
    try:
        request.session['session_timeout'] = time.time() + 100000
        if request.session['session_timeout'] > time.time():
            print(f"time left = {request.session['session_timeout'] - time.time()} seconds")
            request.session['session_timeout'] = time.time() + 100000

            user = User.objects.get(username=request.user)

            user = UsersData.objects.get(user=user)
            btc = float(user.bitcoin_balance)
            eth = float(user.etherum_balance)
            ltc = float(user.litecoin_balance)
            bch = float(user.bitcoin_cash_balance)
            local = float(user.local_currency_balance)

            # handle total balance

            total_balance = btc + local + eth + ltc + bch

            balance = str("{:.1f}".format(total_balance))

            x = ['BITCOIN', 'ETHERUM', 'LITECOIN', 'BITCOINCASH', 'NAIRA']
            btc = str("{:.8f}".format(user.bitcoin_balance))
            eth = str("{:.8f}".format(user.etherum_balance))
            ltc = str("{:.8f}".format(user.litecoin_balance))
            bch = str("{:.8f}".format(user.bitcoin_cash_balance))
            local = str("{:.1f}".format(user.local_currency_balance))
            local = bal_converter(local)
            balance = bal_converter(balance)

            page = 'pages/dashboard.html'
            template = loader.get_template(page)
            context = {'total_balance': total_balance, 'user': str(request.user), 'x': x, 'btc': btc, "eth": eth,
                       'ltc': ltc, "bch": bch,  'naira': f'{local}0',  'integer': balance}
            print(context)
            return HttpResponse(template.render(context, request), status=status.HTTP_200_OK)

        else:
            logout(request)
            return redirect(login_user)

    except Exception as e:
        print(e)
        logout(request)
        return redirect(login_user)


@api_view(['GET', 'POST'])
def register(request):
    reg_form = RegForm

    if request.method == 'GET':
        form = reg_form(None)
        page = 'pages/register.html'
        template = loader.get_template(page)
        logout(request)
        return HttpResponse(template.render({'form': form}, request), status=status.HTTP_200_OK)

    if request.method == 'POST':
        data = request.POST
        ref = request.POST.get('referral_email', '')
        form = reg_form(request.POST)

        if form.is_valid():
            info = form.save(commit=False)

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            email = form.cleaned_data['email']
            try:
                User.objects.get(email=email)
                context = {'error': f'email {email} already exists',
                           'message': 'please try again with a  different email'}
                return Response(context, status=status.HTTP_406_NOT_ACCEPTABLE)

            except Exception as e:
                print(e)
                print('email available to be used')
                info.set_password(password)
                info.save()

                user = User.objects.get(username=username)
                user_data = UsersData(user=user, referral=ref)
                user_data.save()

                history = History(user=user)
                history.save()

                context = {'message': 'Registration successful',
                           'data': data}
                user = authenticate(username=username, password=password)
                if user is not None:
                    print(f'authenticated={request.user.is_authenticated}')
                    login(request, user)
                    print(f'authenticated={request.user.is_authenticated}')
                    context['logged in'] = str(request.user)
                    return redirect(login_user)

                else:
                    return Response({'an error occurred'}, status=status.HTTP_401_UNAUTHORIZED)

        return Response(form.errors, status=status.HTTP_406_NOT_ACCEPTABLE)

    else:
        return Response('invalid request', status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def logout_view(request):
    logout(request)
    return redirect(login_user)


@api_view(['GET'])
def confirm(request):
    page = 'pages/confirm.html'
    template = loader.get_template(page)
    return HttpResponse(template.render({'header': 'TESTING confirm VIEW'}, request), status=status.HTTP_200_OK)


def services(request):
    page = 'test.html'
    template = loader.get_template(page)
    return HttpResponse(template.render({'header': 'TESTING SERVICES VIEW'}, request), status=status.HTTP_200_OK)


def settings(request):
    page = 'pages/settings.html'
    template = loader.get_template(page)
    return HttpResponse(template.render({'header': 'TESTING SERVICES VIEW'}, request), status=status.HTTP_200_OK)
