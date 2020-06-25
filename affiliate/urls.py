from django.urls import path
from . import views

urlpatterns = [
    path('', views.info, name='info'),
    path('currency-type/', views.payment_method, name='method'),
    path('payment/', views.payment, name='payment'),
    path('charge/', views.debit_user, name='charge'),
    path('upgrade/', views.upgrade, name='upgrade'),
    path('withdraw/', views.withdraw, name='withdraw')

]
