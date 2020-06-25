from django.urls import path
from . import views

urlpatterns = [
    path('crypto/<currency>', views.crypto, name='crypto'),
    path('platform/bitcoin', views.btc_select_platform, name='btc_platform'),
    path('platform/<currency>', views.select_other_platform, name='select_other_platform'),
    path('receive/', views.receive, name='receive'),
    path('send/', views.send, name='send'),
    path('send/confirm/', views.check, name='check'),
]
