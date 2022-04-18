import re
import requests
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.reverse import reverse
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import *
from rest_framework_simplejwt import *
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


@swagger_auto_schema(methods=['POST'], request_body=ChangePassSerializer,
                     responses={200: "{'status': 'success'}",
                                404: "{'status': 'Incorrect Password'}"
                                + "\n{'status': 'New Password not match'}"
                                + "\n{'status': 'Password not strong enough'}"})
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def changePassword(request):
    username = request.user
    new_password = request.data.get('new_password')
    rnew_password = request.data.get('rnew_password')
    user = User.objects.get(username=username)
    if user.check_password(request.data.get('password')) == False:
        return Response({'status': 'Incorrect Password'})
    else:
        if not new_password == rnew_password:
            return Response({'status': 'New Password not match'})
        elif not validpassword(new_password):
            return Response({'status': 'Password not strong enough'})
    user.set_password(new_password)
    user.save()
    return Response({'status': 'success'})


@swagger_auto_schema(methods=['POST'], request_body=UpdateUserSerializer,
                     responses={200: "{'status': 'success'}"})
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def updateUser(request):
    username = request.user
    user = request.data
    User.objects.filter(username=username).update(
        email=user['email'], first_name=user['first_name'], last_name=user['last_name'])
    userid = User.objects.get(username=username).id
    if user['default_address'] != '':
        Profile.objects.filter(user_id=userid).update(
            default_address=user['default_address'])
    if user['ship_address'] != '':
        Profile.objects.filter(user_id=userid).update(
            default_address=user['ship_address'])
    if type(user['img']) == type(''):
        Profile.objects.filter(user_id=userid).update(img=user['img'])
    return Response({'status': 'success'})


@swagger_auto_schema(methods=['GET'], request_body=None, responses={200: "List of products"})
@api_view(['GET'])
def products(request):
    queryset = Product.objects.all()
    serializers = ProductSerializer(queryset, many=True, context={
                                    'request': request}).data
    return Response(serializers)


@swagger_auto_schema(methods=['GET'], request_body=None, responses={200: "Detail of product by code"})
@api_view(['GET'])
def detailProduct(request, code):
    queryset = Product.objects.filter(product_code=code)
    serializers = ProductSerializer(queryset, many=True, context={
                                    'request': request}).data[0]
    return Response(serializers)


@swagger_auto_schema(methods=['POST'], request_body=SearchSerializer,
                     responses={200: "List of products have name like query.",
                                404: "{'status': 'failed'}"})
@api_view(['POST'])
def searchProducts(request):
    filterdata = "%" + request.data.get('name') + "%"
    try:
        queryset = Product.objects.raw(
            'SELECT * FROM core_product WHERE name LIKE %s', [filterdata])
        serializers = ProductSerializer(
            queryset, many=True, context={'request': request})
        return Response(serializers.data)
    except:
        return Response({'status': 'failed'})
