import random
from boxes_app import serializers
from boxes_app import signals
from boxes_app.models import (
    User,
    Box,
    UserBox,
    UserBalance,
    Operation,
)
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from drf_yasg.utils import swagger_auto_schema


@swagger_auto_schema(
    method="get",
    operation_description="Get available boxes",
)
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


@swagger_auto_schema(
    method="get",
    operation_description="Get box info by box id",
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


@swagger_auto_schema(
    method="post",
    operation_description="Buy box using user_id and box_id",
)
@api_view(["POST"])
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
                signals.box_is_closed.send(None, box_id=box.id)

            box.save()

            # Create UserBox
            user = User.objects.get(id=user_id)
            user_box_existing = UserBox.objects.filter(user=user, box=box).first()
            if not user_box_existing:
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
