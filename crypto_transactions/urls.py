from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('receive/', views.receive, name='receive'),
    path('send/', views.send, name='send'),
    path('send/confirm/', views.check, name='check'),
]
