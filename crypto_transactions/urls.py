from django.urls import path
from . import views

urlpatterns = [
    path('crypto/<currency>', views.crypto, name='crypto'),
    path('bitcoin/platform', views.btc_select_platform, name='btc_select_platform'),
    path('receive/', views.receive, name='receive'),
    path('send/', views.send, name='send'),
    path('send/confirm/', views.check, name='check'),
]
