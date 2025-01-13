"""
View for the user API.
"""
from rest_framework import generics, authentication, permissions, status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import PermissionDenied

from django.contrib.auth import get_user_model
from user.serializers import (UserSerializer, AuthTokenSerializer, UserRegisterSerializer, DeleteUserSerializer)


class CreateUserView(generics.CreateAPIView):
    """ Create a new user in the system """
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """ Create a new auth token for the user """
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    """ Manage the authenticated user """
    serializer_class = UserSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    """ We want to make sure that the user is authenticated before they can access this endpoint. """ # noqa
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self):
        """ Retrieve and return authenticated user """
        return self.request.user


class UserRegisterView(generics.CreateAPIView):
    """ Register a new user in the system """
    serializer_class = UserRegisterSerializer
    authentication_classes = ()
    permission_classes = ()
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class DeleteUserView(APIView):
    """ Delete a user in the system """
    serializer_class = DeleteUserSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def delete(self, request):
        # Check if the authenticated user is a superuser
        if not request.user.is_superuser:
            raise PermissionDenied({"error": "You do not have permission to perform this action."})

         # Get email from query params
        email = request.query_params.get('email')
        if not email:
            return Response({'error': 'Email is required'}, status=status.HTTP_400_BAD_REQUEST)

         # Fetch and delete the user
        user = get_user_model().objects.filter(email=email).first()
        if not user:
            return Response({'error': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)

        user.delete()
        return Response({'message': 'User deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

