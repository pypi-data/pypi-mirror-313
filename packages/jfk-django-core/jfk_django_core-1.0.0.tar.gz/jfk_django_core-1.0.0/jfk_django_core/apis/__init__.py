from knox.auth import TokenAuthentication
from rest_framework import permissions
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.views import APIView

from .jfk_authentication import *


class BaseAPIView(APIView):
    """Custom API View for all API Views in this file."""

    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [SessionAuthentication, TokenAuthentication, BasicAuthentication]
