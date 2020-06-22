from django.urls import path
from . import views


urlpatterns = [
    path('', views.home_page, name='home_page'),
    path('register', views.register, name='register'),
    path('login', views.login_user, name='login'),
    path('dash', views.dash, name='dash'),
    path('logout', views.logout_view, name='logout')
]
