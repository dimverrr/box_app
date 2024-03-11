from rest_framework import serializers
from .models import User, Box, UserNotification, UserBalance, Operation, UserBox


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"


class BoxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Box
        fields = "__all__"


class UserBalanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBalance
        fields = "__all__"


class OperationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Operation
        fields = "__all__"


class UserNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserNotification
        fields = "__all__"


class UserBoxSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBox
        fields = "__all__"
