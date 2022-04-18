from .serializers import MyTokenObtainPairSerializer, RegisterSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework import status

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

class Register(APIView):
    permission_classes = [AllowAny,]

    def post(self, request):
        data = request.data
        serializer = RegisterSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        print(serializer.data)

        payload = {
            'usuario': serializer.data.get('username'),
            'nombre': serializer.data.get('first_name'),
            'apellido': serializer.data.get('last_name'),
            'email': serializer.data.get('email')
        }

        return Response(payload, status=status.HTTP_201_CREATED)
