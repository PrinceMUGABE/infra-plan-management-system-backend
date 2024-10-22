from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from .models import User
from .serializers import UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import authenticate, login
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError


# Signup Function
@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def send_welcome_email(user):
    subject = 'Welcome to Our Platform'
    message = f'''Hi {user.first_name},

Welcome to our platform! We are excited to have you on board.'''
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [user.email,]
    send_mail(subject, message, email_from, recipient_list)




# Login Function
User = User

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    phone = request.data.get('phone')
    password = request.data.get('password')
    
    
    # Check if user exists
    try:
        user = User.objects.get(phone=phone)
    except User.DoesNotExist:
        return Response({'detail': 'No account found with this phone'}, status=status.HTTP_404_NOT_FOUND)
    
    # Validate password
    if not user.check_password(password):
        return Response({'detail': 'Incorrect password'}, status=status.HTTP_401_UNAUTHORIZED)
    
    # If we get here, both email and password are correct
    refresh = RefreshToken.for_user(user)
    user_data = UserSerializer(user).data
    return Response({
        'user': user_data,
        'refresh': str(refresh),
        'access': str(refresh.access_token)
        
    })


# Get User by ID
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_by_id(request, id):
    try:
        user = User.objects.get(id=id)
        serializer = UserSerializer(user)
        return Response(serializer.data)
    except User.DoesNotExist:
        return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

# Get User by Username
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_by_username(request, username):
    try:
        user = User.objects.get(username=username)
        serializer = UserSerializer(user)
        return Response(serializer.data)
    except User.DoesNotExist:
        return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

# Get User by Email
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_by_email(request, email):
    try:
        user = User.objects.get(email=email)
        serializer = UserSerializer(user)
        return Response(serializer.data)
    except User.DoesNotExist:
        return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

# Get All Users
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_users(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response({"users": serializer.data})  # Ensure users are wrapped in an object




@api_view(['PUT'])
@permission_classes([IsAdminUser])
def update_user_by_id(request, id):
    try:
        user = User.objects.get(id=id)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
    
    
    
    
# Delete User by ID
@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def delete_user_by_id(request, id):
    try:
        user = User.objects.get(id=id)
        user.delete()
        return Response({'detail': 'User deleted successfully'}, status=status.HTTP_204_NO_CONTENT)
    except User.DoesNotExist:
        return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)







from django.db import models  # Add this import for Q objects
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import User  # Ensure to import your User model
from .serializers import UserSerializer  # Ensure to import your UserSerializer

@api_view(['PUT'])
@permission_classes([IsAuthenticated])
def update_user_by_email_or_username(request, identifier):
    try:
        user = User.objects.get(models.Q(email=identifier) | models.Q(username=identifier))
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    except User.DoesNotExist:
        return Response({'detail': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
