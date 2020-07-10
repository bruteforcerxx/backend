from rave_python.rave_exceptions import RaveError, IncompletePaymentDetailsError,\
  CardChargeError, TransactionVerificationError, ServerError, CardChargeError, TransactionValidationError
from rave_python.rave_payment import Payment
from rave_python.rave_misc import generateTransactionReference, getTypeOfArgsRequired, updatePayload
from rave_python import Rave
import time

# Create your tests here.
public_key = "FLWPUBK_TEST-a1390d9bb18fdb3c725be4c0becf9230-X"
secret_key = "FLWSECK_TEST-0669d07232f71539b6f24be07fb31c5f-X"

start = time.time()
rave = Rave(public_key, secret_key, usingEnv=False)

# Payload with pin
payload = { "cardno": "5531886652142950",
  "cvv": "564",
  "expirymonth": "09",
  "expiryyear": "32",
  "amount": "20000",
  "email": "mike@gmail.com",
  "phonenumber": "0902620185",
  "firstname": "dan",
  "lastname": "mike",
  "IP": "355426087298442",
}

Pin = 3310
OTP = 12345

res = rave.Card.charge(payload)
print(res)

arg = getTypeOfArgsRequired(res["suggestedAuth"])
first = time.time() - start
print(first)
print(arg)

start2 = time.time()
updatePayload(res["suggestedAuth"], payload, pin="3310")
res = rave.Card.charge(payload)
start_2 = time.time() - start2
print(start_2)

print(res)

start2 = time.time()

# rave.Card.validate(res["flwRef"], "12345")
res = rave.Card.verify("FLW-MOCK-f6a5ad7946930356a38cefa6be3c43a8")
print(res)

start_2 = time.time() - start2
print(start_2)

print(res["transactionComplete"])
# if res["validationRequired"]:

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

print('start1')
res = rave.Account.charge(payload)
print(res)
if res["authUrl"]:
    print('start2')
    print(res["authUrl"])

if res["validationRequired"]:
    print('start3')
    rave.Account.validate(res["flwRef"], "12345")

res = rave.Account.verify(res["txRef"])
print('start4')
print(res)

















try:

   pass

except CardChargeError as e:
    print(e.err["errMsg"])
    print(e.err["flwRef"])

except TransactionValidationError as e:
    print(e.err)
    print(e.err["flwRef"])

except TransactionVerificationError as e:
    print(e.err["errMsg"])
    print(e.err["txRef"])