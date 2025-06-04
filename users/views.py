from django.shortcuts import render
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import UserCreateSerializer, UserSerializer, UserUpdateSerializer
from .models import User
import jwt, datetime

# Create your views here.
class RegisterView(APIView):
    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

 
class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']

        user = authenticate(request, username=email, password=password)

        if user is None:
            raise AuthenticationFailed('Credenciales incorrectas.')

        payload = {
            'id': user.id,
            'expired': int((datetime.datetime.utcnow() + datetime.timedelta(minutes=60)).timestamp()),
            'iat': int(datetime.datetime.utcnow().timestamp()),
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')

        response = Response()
        response.set_cookie(
            key='jwt',
            value=token,
            httponly=True
        )
        # response.data = {
        #     'jwt': token
        # }
        return response


class UserView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('No autenticado')

        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Sesión expirada')
        except jwt.DecodeError:
            raise AuthenticationFailed('Token inválido')

        user = User.objects.get(id=payload['id'])
        serializer = UserCreateSerializer(user)
        return Response(serializer.data)


class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'Sesión cerrada con exito.'    
        }
        return response


class UserList(APIView):
    def get(self, request):
        all_users = User.objects.all()
        serializer = UserSerializer(all_users, many=True)
        data = {
            'users': serializer.data
        }
        return Response(data)
    

class UserEdit(APIView):
    def put(self, request):
        user = User.objects.get(id=request.data.get('id'))
        serializer = UserUpdateSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Usuario actualizado correctamente.'})
