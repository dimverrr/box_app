from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from boxes_app.models import (
    UserBalance,
)
from boxes_app import serializers
from drf_yasg.utils import swagger_auto_schema


@swagger_auto_schema(
    method="get",
    operation_description="Get user balance by user id",
)
@api_view(["GET"])
def get_user_balance(request, user_id):
    user_balance = UserBalance.objects.filter(user_id=user_id).all()
    if not user_balance:
        return Response(
            {"User does not have any coins"}, status=status.HTTP_404_NOT_FOUND
        )
    serializer = serializers.UserBalanceSerializer(user_balance, many=True)

    return Response(
        {"Balance": [balance for balance in serializer.data]}, status=status.HTTP_200_OK
    )
