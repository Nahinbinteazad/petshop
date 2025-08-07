from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from .serializers import RegisterSerializer
from django.contrib.auth.models import User
import uuid

@api_view(['POST'])
def register_view(request):
    data = request.data.copy()
    data['username'] = data.get('name')  # 🛠 Map 'name' to 'username' (Django needs this)

    serializer = RegisterSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
    
    print("❌ Registration Error:", serializer.errors)  # Optional debug print
    return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def login_view(request):
    email = request.data.get('email')
    password = request.data.get('password')

    try:
        user = User.objects.get(email=email)
        user_auth = authenticate(username=user.username, password=password)
        if user_auth:
            fake_token = str(uuid.uuid4())  # 🧪 Replace with JWT in future
            return Response({'token': fake_token}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    except User.DoesNotExist:
        return Response({'error': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)
