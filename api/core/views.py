import re
import requests
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import *
# from rest_framework_simplejwt import *
from .serializers import *
from .models import *
from drf_yasg.utils import swagger_auto_schema


def validpassword(p):
    if len(p) < 6 or not re.search("[a-z]", p) or not re.search("[0-9]", p):
        return False
    return True


@swagger_auto_schema(methods=['POST'], request_body=RegisterSerializer,
                     responses={200: "{'status': 'register success'}",
                                404: "{'status': 'You must enter all fields'}"
                                + "\n{'status': 'User alrealdy exist'}"
                                + "\n{'status': 'Password contains at least 6 characters. It must contain letters and numbers.'}"
                                + "\n{'status': 'Password not match'}"})
@api_view(['POST'])
def register(request):
    user = request.data
    username = user['username']
    email = user['email']
    firstname = user['firstname']
    lastname = user['lastname']
    password = user['password']
    rpassword = user['re_password']
    if username == '' or email == '' or password == '' or rpassword == '':
        return Response({'status': 'You must enter all fields'})
    if User.objects.filter(username=username).exists():
        return Response({'status': 'User alrealdy exist'})
    elif User.objects.filter(email=email).exists():
        return Response({'status': 'Email alrealdy exist'})
    elif validpassword(password) == False:
        return Response({'status': 'Password contains at least 6 characters. It must contain letters and numbers.'})
    elif rpassword != password:
        return Response({'status': 'Password not match'})
    else:
        user = User.objects.create_user(username, email, password)
        user.last_name = lastname
        user.first_name = firstname
        user.save()
        Cart.objects.create(user=user)
        Profile.objects.create(user=user)
        return Response({'status': 'register success'})


@swagger_auto_schema(methods=['POST'], request_body=LoginSerializer,
                     responses={200: "{'access': token,\n'refresh': token,\n'username': username,\n'status': 'Login success'}",
                                404: "{'detail': 'Incorrect authentication credentials.'}"})
@api_view(['POST'])
def login(request):
    # serializer_class = LoginSerializer
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


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    return Response()
