from django.contrib import admin
from .models import (
    UserBox,
    UserNotification,
    UserBalance,
    User,
    Box,
    Coin,
    Operation,
    Notification,
)

# Register your models here.
models = [
    UserBox,
    UserNotification,
    UserBalance,
    User,
    Box,
    Coin,
    Operation,
    Notification,
]
admin.site.register(models)
