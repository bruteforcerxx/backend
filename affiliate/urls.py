from django.urls import path
from . import views

urlpatterns = [
    path('', views.info, name='info'),
    path('charge/', views.debit_user, name='charge'),
    path('upgrade/', views.upgrade, name='upgrade'),
    path('withdraw/', views.withdraw, name='withdraw'),
    path('test/', views.test, name='test'),

]
