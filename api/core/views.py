import requests
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import *
# from rest_framework_simplejwt import *


@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    if not User.objects.filter(username=username).exists() or User.objects.filter(email=username).exists():
        raise exceptions.AuthenticationFailed()
    if User.objects.filter(email=username).exists():
        username = User.objects.get(email=username).username
    user = authenticate(username=username, password=password)
    if user is None:
        raise exceptions.AuthenticationFailed()
    token_endpoint = reverse(viewname='token_obtain_pair', request=request)
    token = requests.post(token_endpoint, data=request.data).json()
    response = Response()
    response.data = {
        'access': token.get('access'),
        'refresh': token.get('refresh'),
        'username': username,
        'status': 'Login success'
    }
    return response
