from .serializer import UserSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User, Group
from rest_framework.permissions import IsAuthenticated
from .permissions import (
    IsAdmin,
    IsModerator,
    IsUser
)


class RegisterUserView(APIView):
    def post(self,request):
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            user_group, _ = Group.objects.get_or_create(name="User")
            user.groups.add(user_group)
            user.save()
            return Response({"message":"User Registered Successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterAdminView(APIView):
    
    def post(self, request):

        if User.objects.filter(groups__name='Admin').exists():
            return Response({'error': 'An admin already exists.'}, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Assign the 'Admin' group to the user
            admin_group = Group.objects.get(name='Admin')
            user_group = Group.objects.get(name='User')
            user.groups.add(admin_group)
            user.groups.add(user_group)
            user.save()
            return Response({'message': 'Admin created successfully.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):

        refresh_token = request.data.get('refresh')

        if not refresh_token:
            return Response({"message": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'message': "Successfully logged out"}, status=status.HTTP_205_RESET_CONTENT)
        except:
            return Response({"detail":"Provide Vaild token"}, status=status.HTTP_400_BAD_REQUEST)

class AssignRoleView(APIView):
    permission_classes = [IsAuthenticated, IsAdmin] 

    def patch(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        new_role = request.data.get('role')
        try:
            group = Group.objects.get(name=new_role)
        except Group.DoesNotExist:
            return Response({'error': 'Invalid role. Only existing roles (Admin, Moderator, User) can be assigned.'}, status=status.HTTP_400_BAD_REQUEST)

        # Add user to the selected role (group)
        user.groups.add(group)
        user.save()

        return Response({'message': f'User role updated to {new_role}.'}, status=status.HTTP_200_OK)

# accessing the views using only particular role
class ManageResources(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]

    def get(self, request):
        return Response({"message": "You are Eligible for this Resources!"}, status=status.HTTP_200_OK)

class MyResources(APIView):
    permission_classes = [IsAuthenticated, IsUser]

    def get(self, request):
        return Response({"message": "You are Eligible for this Resources!"}, status=status.HTTP_200_OK)

class EditResources(APIView):
    permission_classes = [IsAuthenticated, IsModerator]

    
    def get(self, request):
        return Response({"message": "You are Eligible for this Resources!"}, status=status.HTTP_200_OK)

