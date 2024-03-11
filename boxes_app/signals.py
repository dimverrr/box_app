from django.dispatch import receiver
from django.dispatch import Signal
from .models import UserBox, UserNotification, Notification
from django.db import transaction


box_is_closed = Signal()
box_is_closed.providing_args = ["box_id"]


@receiver(box_is_closed)
def closed_box_notification(sender, **kwargs):
    box_id = kwargs["box_id"]
    notification = Notification.objects.filter(action="close_box").first()

    user_boxes = UserBox.objects.filter(box_id=box_id).all()

    with transaction.atomic():
        for user_box in user_boxes:
            user_box.is_available = False
            user_box.save()

            user_notification = UserNotification(
                user=user_box.user, notification=notification
            )
            user_notification.save()


# Connecting recievers & signals
box_is_closed.connect(closed_box_notification)
