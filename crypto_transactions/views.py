from django.http import HttpResponse
from .models import TransferForm
from rest_framework import status
from django.template import loader
from .process import coinbase, luno, local, get_address
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from home.models import UsersData
from django.shortcuts import redirect
import json

# Create your views here.


@api_view(['GET', 'POST'])
def index(request):
    page = 'selection.html'
    template = loader.get_template(page)
    return HttpResponse(template.render({'message': 'make a selection'}, request), status=status.HTTP_200_OK)


@api_view(['GET'])
def receive(request):
    page = 'address.html'
    template = loader.get_template(page)
    user = 'test'
    context = {'address': get_address(user)}
    return HttpResponse(template.render(context, request), status=status.HTTP_200_OK)


@api_view(['GET'])
def send(request):
    form_model = TransferForm
    form = form_model(None)
    page = 'request.html'
    template = loader.get_template(page)
    return HttpResponse(template.render({'form': form}, request), status=status.HTTP_200_OK)


@api_view(['POST', 'GET'])
def check(request):

    if request.method == 'POST':
        form = TransferForm(request.POST)
        tx_hash = request.POST.get('csrfmiddlewaretoken', '')
        page = 'confirm.html'
        template = loader.get_template(page)

        if form.is_valid():
            print('FORM IS VALID')
            transaction = form.save(commit=False)
            transaction.tx_hash = tx_hash
            to = form.cleaned_data['destination']
            amount = float(form.cleaned_data['amount'])
            desc = form.cleaned_data['description']
            platform = form.cleaned_data['platform']

            context = {'to': to, 'amount': amount, 'desc': desc, 'platform': platform, 'user': str(request.user)}
            request.session['data'] = context
            print(context)

            return HttpResponse(template.render(context, request), status=status.HTTP_200_OK)

        context = {'form validation error': form.errors, 'data': request.POST}
        return Response(context, status=status.HTTP_406_NOT_ACCEPTABLE)

    if request.method == 'GET':
        params = request.session['data']
        platform = params['platform']
        user = params['user']
        amount = params['amount']

        if User.objects.get(username=user):
            user = User.objects.get(username=user)
            user = UsersData.objects.get(user=user)
            balance = float(user.bitcoin_balance)
            print(user, balance)

            if balance >= float(amount):
                response = 'request not resolved'

                if platform == 'blockchain':
                    response = coinbase(params)
                elif platform == 'coinbase':
                    response = coinbase(params)
                elif platform == 'luno':
                    response = luno(params)
                elif platform == 'axemo':
                    response = local(params)

                print(response)

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
