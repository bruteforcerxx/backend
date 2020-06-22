from django.urls import path
from . import views

urlpatterns = [
    path('bitcoin', views.index_btc, name='index_btc'),
    path('bitcoin/platform', views.btc_select_platform, name='btc_select_platform'),
    path('etherum', views.index_eth, name='index_eth'),
    path('litecoin', views.index_ltc, name='index_ltc'),
    path('bitcoin_cash', views.index_bch, name='index_bch'),
    path('receive/', views.receive, name='receive'),
    path('send/', views.send, name='send'),
    path('send/confirm/', views.check, name='check'),
]
