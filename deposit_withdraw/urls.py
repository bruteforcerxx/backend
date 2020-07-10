from django.urls import path
from . import views

urlpatterns = [
    path('NAIRA', views.naira_account, name='naira'),
    path('response/<section>', views.res, name='response'),
    path('processing', views.process, name='process'),
    path('card-deposit', views.deposit_card, name='dep-card'),
    path('validate-otp', views.otp_validate, name='otp-validate'),
    path('validate-3Dsecure/', views.url_validate, name='url-validate'),
]
