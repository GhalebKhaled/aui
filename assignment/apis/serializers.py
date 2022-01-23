import rest_framework.serializers

from .. import models


class UsersSerializer(rest_framework.serializers.ModelSerializer):
    class Meta:
        model = models.User
        fields = '__all__'
