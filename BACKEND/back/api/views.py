# from rest_framework.decorators import api_view
# from rest_framework.response import Response
# from rest_framework import status
# from django.contrib.auth import authenticate
# from .serializers import RegisterSerializer
# from django.contrib.auth.models import User
# import uuid

# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import IsAuthenticated

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def get_profile(request):
#     user = request.user
#     return Response({
#         "name": user.username,
#         "email": user.email,
#         "avatar": "",  # You can later use a real avatar field or model
#     })

# @api_view(['POST'])
# def register_view(request):
#     data = request.data.copy()
#     data['username'] = data.get('name')  # 🛠 Map 'name' to 'username' (Django needs this)

#     serializer = RegisterSerializer(data=data)
#     if serializer.is_valid():
#         serializer.save()
#         return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
    
#     print("❌ Registration Error:", serializer.errors)  # Optional debug print
#     return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

# @api_view(['POST'])
# def login_view(request):
#     email = request.data.get('email')
#     password = request.data.get('password')

#     try:
#         user = User.objects.get(email=email)
#         user_auth = authenticate(username=user.username, password=password)
#         if user_auth:
#             fake_token = str(uuid.uuid4())  # 🧪 Replace with JWT in future
#             return Response({'token': fake_token}, status=status.HTTP_200_OK)
#         else:
#             return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
#     except User.DoesNotExist:
#         return Response({'error': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from .serializers import RegisterSerializer


# ✅ GET profile (auth required)
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_profile(request):
    user = request.user
    return Response({
        "name": user.username,
        "email": user.email,
        "avatar": "",  # Optional
    })


# ✅ REGISTER view (no auth required)
@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    data = request.data.copy()
    data['username'] = data.get('name')  # Map name to username

    serializer = RegisterSerializer(data=data)
    if serializer.is_valid():
        user = serializer.save()
        # Auto-create token (optional if you switch to JWT later)
        Token.objects.create(user=user)
        return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)

    print("❌ Registration Error:", serializer.errors)
    return Response({'error': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


# ✅ LOGIN view (no auth required)
@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    email = request.data.get('email')
    password = request.data.get('password')

    try:
        user = User.objects.get(email=email)
        user_auth = authenticate(username=user.username, password=password)
        if user_auth:
            token, _ = Token.objects.get_or_create(user=user_auth)
            return Response({'token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
    except User.DoesNotExist:
        return Response({'error': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)
