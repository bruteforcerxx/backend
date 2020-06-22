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
import json

# Create your views here.


@api_view(['GET'])
def home_page(request):
    page = 'home.html'
    template = loader.get_template(page)
    return HttpResponse(template.render({'header': 'TESTING ABOUT VIEW'}, request), status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
def login_user(request):
    if request.method == 'GET':
        page = 'login.html'
        template = loader.get_template(page)
        return HttpResponse(template.render({'message': 'make a selection'}, request), status=status.HTTP_200_OK)

    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')

        user = authenticate(username=username, password=password)
        print('#'*100)
        print(user)
        if user is not None:
            login(request, user)
            print('#' * 100)
            print(user)
            return redirect(dash)
        else:
            error = {'error': 'non-existent  account',
                     'message': 'the credentials you provided are not valid. Please cross-check and try again or '
                                'register a new account if you do not have an account'}
            return Response(error, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['GET', 'POST'])
def dash(request):
    page = 'dash.html'
    template = loader.get_template(page)
    user = User.objects.get(username=request.user)
    print(user)
    user = UsersData.objects.get(user=user)
    btc = float(user.bitcoin_balance)
    local = float(user.local_currency_balance)
    total_balance = btc + local
    context = {'total_balance': total_balance, 'user': str(request.user)}
    return HttpResponse(template.render(context, request), status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
def register(request):
    reg_form = RegForm

    if request.method == 'GET':
        form = reg_form(None)
        page = 'reg.html'
        template = loader.get_template(page)
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
                    return redirect(dash)
                else:
                    return Response({'an error occurred'}, status=status.HTTP_401_UNAUTHORIZED)

        return Response(form.errors, status=status.HTTP_406_NOT_ACCEPTABLE)

    else:
        return Response('invalid request', status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def logout_view(request):
    logout(request)
    return redirect(home_page)


def about(request):
    page = 'test.html'
    template = loader.get_template(page)
    return HttpResponse(template.render({'header': 'TESTING ABOUT VIEW'}, request), status=status.HTTP_200_OK)


def services(request):
    page = 'test.html'
    template = loader.get_template(page)
    return HttpResponse(template.render({'header': 'TESTING SERVICES VIEW'}, request), status=status.HTTP_200_OK)
