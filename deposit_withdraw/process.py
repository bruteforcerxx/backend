from rave_python.rave_exceptions import RaveError, IncompletePaymentDetailsError,\
  CardChargeError, TransactionVerificationError, ServerError, CardChargeError, TransactionValidationError
from rave_python.rave_payment import Payment
from rave_python.rave_misc import generateTransactionReference, getTypeOfArgsRequired, updatePayload
from rave_python import Rave
import time
from django.contrib.auth.models import User
from home.models import UsersData
from django.contrib.sessions.backends.db import SessionStore
import requests
import json

public_key = "FLWPUBK_TEST-a1390d9bb18fdb3c725be4c0becf9230-X"
secret_key = "FLWSECK_TEST-0669d07232f71539b6f24be07fb31c5f-X"



def buy_crypto():
    pass



def sell_crypto():
    pass


def deposit_money_cad(payload, pin):
    pin = f"{pin}"
    print(pin)

    try:
        rave = Rave(public_key, secret_key, usingEnv=False)

        res = rave.Card.charge(payload)
        print(res)

        if res["suggestedAuth"]:
            arg = getTypeOfArgsRequired(res["suggestedAuth"])

            if arg == "pin":
                updatePayload(res["suggestedAuth"], payload, pin=pin)

            res = rave.Card.charge(payload)
            print(res)

        if res["validationRequired"]:

            if res["authUrl"] is None:
                return [res["txRef"], res["flwRef"], 'otp required']

            else:
                return [res["txRef"], res["authUrl"], '3D secure validation']

    except Exception as e:
        return str(e)


def otp_validation(res, otp, user):
    otp = f"{otp}"

    try:

        rave = Rave(public_key, secret_key, usingEnv=False)
        rave.Card.validate(res[1], otp)
        response = rave.Card.verify(res[0])
        print(response)
        print(res)
        print(float(res[2]))
        if response["transactionComplete"]:
            user = User.objects.get(username=user)
            user = UsersData.objects.get(user=user)
            print(user)
            print(user.local_currency_balance)
            user.local_currency_balance += float(res[2])
            print(user.local_currency_balance)
            user.save()
            return 'success'
        else:
            return 'failed'

    except Exception as e:
        return e


def url_auth(data, response, user):
    status = json.loads(response)
    if status['status'] == 'successful':
        rave = Rave(public_key, secret_key, usingEnv=False)

        response = rave.Card.verify(data[0])
        print(response)

        if response["transactionComplete"]:
            user = User.objects.get(username=user)
            user = UsersData.objects.get(user=user)
            print(user)
            print(user.local_currency_balance)
            user.local_currency_balance += float(data[1])
            print(user.local_currency_balance)
            user.save()
            return 'success'
        else:
            return 'failed'

    else:
        return 'failed'




def deposit_money_account():
    rave = Rave(public_key, secret_key, usingEnv=False)

    payload = {
        "accountbank": "044",  # get the bank code from the bank list endpoint.
        "accountnumber": "0690000031",
        "currency": "NGN",
        "country": "NG",
        "amount": "100",
        "email": "test@test.com",
        "phonenumber": "0902620185",
        "IP": "355426087298442",
    }

    res = rave.Account.charge(payload)
    print(res)
    if res["authUrl"]:
        print('start2')
        print(res["authUrl"])

    if res["validationRequired"]:
        print('start3')
        rave.Account.validate(res["flwRef"], "12345")

    res = rave.Account.verify(res["txRef"])
    print(res)



def withdraw_money():
    pass




def load_history():
    pass


def bal_converter(x):
    print(len(x))
    if len(x) == 6:
        a = x[0]
        b = x[1:]
        return f'{a},{b}'
    elif len(x) == 7:
        a = x[:2]
        b = x[2:]
        return f'{a},{b}'
    elif len(x) == 8:
        a = x[:3]
        b = x[3:]
        return f'{a},{b}'
    elif len(x) == 9:
        a = x[0]
        b = x[1:4]
        c = x[4:]
        return f'{a},{b},{c}'
    elif len(x) == 10:
        a = x[:2]
        b = x[2:5]
        c = x[5:]
        return f'{a},{b},{c}'
    elif len(x) == 11:
        a = x[:2]
        b = x[2:5]
        c = x[5:]
        return f'{a},{b},{c}'
    else:
        return x