from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from boxes_app import serializers
from boxes_app.models import User
from drf_yasg.utils import swagger_auto_schema


@swagger_auto_schema(
    method="post",
    request_body=serializers.UserSerializer,
)
@api_view(["POST"])
def create_user(request):
    serializer = serializers.UserSerializer(data=request.data)
    if serializer.is_valid():
        _, created = User.objects.get_or_create(
            username=request.data["username"],
            name=request.data["name"],
            phone_number=request.data["phone_number"],
            email=request.data["email"],
            language=request.data["language"],
            country=request.data["country"],
        )
        if created:
            return Response({"user": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            return Response(
                {"User with this username already exists"},
                status=status.HTTP_409_CONFLICT,
            )
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@swagger_auto_schema(
    method="get",
    operation_description="Get credential object by credential name",
)
@api_view(["GET"])
def get_user(request, user_id):
    user = User.objects.filter(id=user_id).first()
    if not user:
        return Response(
            {"User with id {} was not found".format(user_id)},
            status=status.HTTP_404_NOT_FOUND,
        )
    serializer = serializers.UserSerializer(user)
    return Response({"User": serializer.data}, status=status.HTTP_200_OK)
