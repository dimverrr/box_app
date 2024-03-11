from django.urls import path
from boxes_app.views import (
    user_views,
    user_notification_views,
    balance_views,
    box_views,
    operation_views,
)


urlpatterns = [
    path("api/new_user", user_views.create_user, name="create_user"),
    path("api/get_user/<int:user_id>", user_views.get_user, name="get_user"),
    path("api/box", box_views.get_available_boxes, name="get_available_boxes"),
    path("api/box/<int:box_id>", box_views.get_box_by_id, name="get_box_by_id"),
    path("api/buy_box/<int:user_id>/<int:box_id>", box_views.buy_box, name="buy_box"),
    path(
        "api/user_balance/<int:user_id>",
        balance_views.get_user_balance,
        name="get_user_balance",
    ),
    path(
        "api/user_operations/<int:user_id>",
        operation_views.get_user_operations,
        name="get_user_operations",
    ),
    path(
        "api/user_notifications/<int:user_id>",
        user_notification_views.get_user_notifications,
        name="get_user_notifications",
    ),
    # path(
    #     "api/user_boxes/<int:user_id>",
    #     views.get_user_boxes,
    #     name="get_user_boxes",
    # ),
]
