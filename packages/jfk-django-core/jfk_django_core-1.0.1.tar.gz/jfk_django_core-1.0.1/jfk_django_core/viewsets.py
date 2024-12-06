import logging

from django.contrib.auth.models import User
from knox.auth import TokenAuthentication
from rest_framework import permissions, viewsets
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from . import serializers

log = logging.getLogger(__name__)


class JFKPagination(PageNumberPagination):
    page_size_query_param = "page_size"
    max_page_size = 1000

    def get_paginated_response(self, data):
        return Response(
            {
                "next": self.page.next_page_number() if self.page.has_next() else None,
                "previous": self.page.previous_page_number() if self.page.has_previous() else None,
                "count": self.page.paginator.count,
                "page": self.page.number,
                "results": data,
            },
        )


class JFKViewSet(viewsets.ModelViewSet):
    """API endpoint that allows users to be viewed or edited."""

    pagination_class = JFKPagination
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]


class UserViewSet(JFKViewSet):
    """API endpoint that allows users to be viewed or edited."""

    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer

    def get_queryset(self):
        return super().get_queryset().filter(id=self.request.user.id)
