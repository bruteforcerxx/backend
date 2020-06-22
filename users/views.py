from django.http import HttpResponse, HttpResponseRedirect
from rest_framework import status
from django.template import loader
from rest_framework.response import Response
from rest_framework.decorators import api_view

# Create your views here.


def login(request):
    page = 'selection.html'
    template = loader.get_template(page)
    return HttpResponse(template.render({'message': 'make a selection'}, request), status=status.HTTP_200_OK)


def login(request):
    page = 'selection.html'
    template = loader.get_template(page)
    return HttpResponse(template.render({'message': 'make a selection'}, request), status=status.HTTP_200_OK)


