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

# View for user registration
class RegisterUserView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)

        # Check if the data is valid
        if serializer.is_valid():
            user = serializer.save()
            user_group, _ = Group.objects.get_or_create(name="User")
            user.groups.add(user_group)
            user.save()
            return Response({"message": "User Registered Successfully"}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# View for admin registration
class RegisterAdminView(APIView):
    def post(self, request):
        # Check if an admin already exists
        if User.objects.filter(groups__name='Admin').exists():
            return Response({'error': 'An admin already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        # Initialize the UserSerializer with the data from the request
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            # Save the user and assign them to both the 'Admin' and 'User' groups
            user = serializer.save()
            admin_group = Group.objects.get(name='Admin')
            user_group = Group.objects.get(name='User')
            user.groups.add(admin_group)
            user.groups.add(user_group)
            user.save()
            return Response({'message': 'Admin created successfully.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# View for logging out the user
class LogoutView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated before accessing this view

    def post(self, request):
        # Extract the refresh token from the request data
        refresh_token = request.data.get('refresh')

        # Check if the refresh token is provided
        if not refresh_token:
            return Response({"message": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Blacklist the refresh token to log the user out
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({'message': "Successfully logged out"}, status=status.HTTP_205_RESET_CONTENT)
        except:
            # Return an error if the token is invalid
            return Response({"detail": "Provide Valid token"}, status=status.HTTP_400_BAD_REQUEST)


# Protected view for assigning roles to users
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

        # Add the user to the selected role (group)
        user.groups.add(group)
        user.save()

        return Response({'message': f'User role updated to {new_role}.'}, status=status.HTTP_200_OK)


# Protected view for managing resources (accessible by Admins)
class ManageResources(APIView):
    permission_classes = [IsAuthenticated, IsAdmin]  

    def get(self, request):
        return Response({"message": "You are Eligible for this Resources!"}, status=status.HTTP_200_OK)


# Protected view for viewing resources (accessible by Users)
class MyResources(APIView):
    permission_classes = [IsAuthenticated, IsUser]  

    def get(self, request):
        return Response({"message": "You are Eligible for this Resources!"}, status=status.HTTP_200_OK)


# Protected view for editing resources (accessible by Moderators)
class EditResources(APIView):
    permission_classes = [IsAuthenticated, IsModerator]  

    def get(self, request):
        return Response({"message": "You are Eligible for this Resources!"}, status=status.HTTP_200_OK)
