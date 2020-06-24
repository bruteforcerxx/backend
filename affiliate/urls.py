from django.urls import path
from . import views

urlpatterns = [
    path('', views.info, name='info'),
    path('currency-type/', views.payment_method, name='method'),
    path('payment/<currency>', views.payment, name='payment')
]
