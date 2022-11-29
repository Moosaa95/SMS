from rest_framework import serializers
from .models import Account, Profile


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ["id", "first_name", "last_name"]

