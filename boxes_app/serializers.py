from rest_framework import serializers
from .models import (
    User,
    Box,
    UserNotification,
    UserBalance,
    Operation,
    UserBox,
    Notification,
)


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


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ["id", "action"]


class UserNotificationSerializer(serializers.ModelSerializer):
    notification = NotificationSerializer()

    class Meta:
        model = UserNotification
        fields = ["created_at", "user", "notification"]


class UserBoxSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserBox
        fields = "__all__"
