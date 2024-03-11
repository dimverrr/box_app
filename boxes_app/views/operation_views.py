from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from boxes_app.models import Operation
from boxes_app import serializers
from drf_yasg.utils import swagger_auto_schema


@swagger_auto_schema(
    method="get",
    operation_description="Get user operations by user id",
)
@api_view(["GET"])
def get_user_operations(request, user_id):
    user_operations = Operation.objects.filter(user_id=user_id).all()
    if not user_operations:
        return Response(
            {"User does not have any operations"}, status=status.HTTP_404_NOT_FOUND
        )
    serializer = serializers.OperationsSerializer(user_operations, many=True)

    return Response(
        {"Operations": [operation for operation in serializer.data]},
        status=status.HTTP_200_OK,
    )
