from .models import (
    User,
    Box,
    UserBox,
    Notification,
    UserBalance,
    Operation,
)
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
import random
from . import signals
from . import serializers

# Create your views here.

# USER Views


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


# @api_view(["GET"])
# def get_all_boxes(request):
#     boxes = Box.objects.all()
#     if not boxes:
#         return Response({"There are no boxes"}, status=status.HTTP_404_NOT_FOUND)
#     return Response({"Boxes": boxes}, status=status.HTTP_200_OK)


@api_view(["GET"])
def get_available_boxes(request):
    boxes = Box.objects.filter(is_available=True).all()
    if not boxes:
        return Response(
            {"There are no available boxes"}, status=status.HTTP_404_NOT_FOUND
        )

    serializer = serializers.BoxSerializer(boxes, many=True)

    return Response(
        {"Boxes": [box for box in serializer.data]}, status=status.HTTP_200_OK
    )


@api_view(["GET"])
def get_box_by_id(request, box_id):
    box = Box.objects.filter(id=box_id).first()
    if not box:
        return Response(
            {f"There is no box with id - {box_id}"}, status=status.HTTP_404_NOT_FOUND
        )

    serializer = serializers.BoxSerializer(box)

    return Response({"Box": serializer.data}, status=status.HTTP_200_OK)


@api_view(["PUT"])
def buy_box(request, user_id, box_id):
    box = Box.objects.filter(id=box_id, is_available=True).first()

    if not box:
        return Response(
            {"Box with id {} was not found or not available".format(box_id)},
            status=status.HTTP_404_NOT_FOUND,
        )

    user_balance = UserBalance.objects.filter(
        user_id=user_id, coin_id=box.coin_id
    ).first()

    if not user_balance:
        return Response(
            {f"User with id {user_id} was not found or required coin was not found"},
            status=status.HTTP_404_NOT_FOUND,
        )

    if user_balance.balance < box.attempt_price:
        return Response(
            {f"User with id {user_id} does not have enough coin with id {box.coin_id}"},
            status=status.HTTP_406_NOT_ACCEPTABLE,
        )
    else:
        with transaction.atomic():

            # Calculate user prize
            user_prize = random.randint(1, box.current_sum)

            # Update box balance and attempts
            box.current_sum -= user_prize
            box.current_attempts -= 1
            if box.current_attempts == 0 or box.current_sum == 0:
                box.is_available = False
                signals.box_is_closed.send(box_id=box.id)

            box.save()

            # Create UserBox
            user = User.objects.get(id=user_id)
            user_box = UserBox(user=user, box=box, is_available=box.is_available)
            user_box.save()

            # Create substract operation
            operation_substract = Operation(
                sum=box.attempt_price, user=user, box=box, transaction_type="substract"
            )
            operation_substract.save()

            # Update user balance
            user_balance.balance -= box.attempt_price
            user_balance.balance += user_prize
            user_balance.save()

            # Create add operation
            operation_add = Operation(
                sum=user_prize, user=user, box=box, transaction_type="add"
            )
            operation_add.save()

            return Response(
                {f"Congratulations, you won {user_prize}"}, status=status.HTTP_200_OK
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


@api_view(["GET"])
def get_user_notifications(request, user_id):
    user_notifications = Notification.objects.filter(user_id=user_id).all()
    if not user_notifications:
        return Response(
            {"User does not have any notifications"}, status=status.HTTP_404_NOT_FOUND
        )

    serializer = serializers.NotificationSerializer(user_notifications, many=True)
    return Response(
        {"Notifications": [notification for notification in serializer.data]},
        status=status.HTTP_200_OK,
    )
