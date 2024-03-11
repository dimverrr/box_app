from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from boxes_app.models import UserNotification
from boxes_app import serializers
from drf_yasg.utils import swagger_auto_schema


@swagger_auto_schema(
    method="get",
    operation_description="Get user notifications by user id",
)
@api_view(["GET"])
def get_user_notifications(request, user_id):
    user_notifications = UserNotification.objects.filter(user_id=user_id).all()
    if not user_notifications:
        return Response(
            {"User does not have any notifications"}, status=status.HTTP_404_NOT_FOUND
        )

    serializer = serializers.UserNotificationSerializer(user_notifications, many=True)
    return Response(
        {"Notifications": [notification for notification in serializer.data]},
        status=status.HTTP_200_OK,
    )
