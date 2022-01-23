import logging

import rest_framework.generics
import rest_framework.pagination
import rest_framework.permissions
import rest_framework.response
import rest_framework.status

from . import serializers
from .. import models

log = logging.getLogger(__name__)


class ListUsersView(rest_framework.generics.ListAPIView):
    serializer_class = serializers.UsersSerializer
    pagination_class = rest_framework.pagination.PageNumberPagination
    permission_classes = [rest_framework.permissions.AllowAny]  # TODO implement authentication

    def get_request_ids(self):
        ids = self.request.GET.get('ids')
        return ids.split(',')

    def get(self, request, *args, **kwargs):
        if not self.request.GET.get('ids'):
            return rest_framework.response.Response(
                data={'ids': 'required field'},
                status=rest_framework.status.HTTP_400_BAD_REQUEST
            )
        return super(ListUsersView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        ids = self.get_request_ids()
        return models.User.query_by_ids(ids[:10])

    def filter_queryset(self, users_qs):
        ids = self.get_request_ids()
        ids = super(ListUsersView, self).filter_queryset(ids)
        return models.User.query_by_ids(ids)

