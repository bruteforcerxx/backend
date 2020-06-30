from django.urls import path
from . import views

urlpatterns = [
    path('crypto/<currency>', views.crypto, name='crypto'),
    path('receive/', views.receive, name='receive'),
    path('qr/', views.qrcam, name='qr'),
    path('send/confirm/', views.check, name='check'),
]
