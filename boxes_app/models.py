from django.db import models
from django.utils import timezone

# Create your models here.


class User(models.Model):
    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=20, help_text="Enter phone number")
    email = models.EmailField(max_length=50)
    language = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    created_at = models.TimeField(default=timezone.now)

    def __str__(self) -> str:
        return self.username


class Coin(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    rate = models.IntegerField()
    amount = models.IntegerField()
    is_available = models.BooleanField(default=True)
    created_at = models.TimeField(default=timezone.now)

    def __str__(self) -> str:
        return self.name


class Box(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    body = models.CharField(max_length=50)
    sum = models.IntegerField()
    attempts = models.IntegerField()
    current_sum = models.IntegerField()
    current_attempts = models.IntegerField()
    attempt_price = models.IntegerField()
    coin = models.ForeignKey(Coin, on_delete=models.CASCADE)
    is_available = models.BooleanField(default=True)
    created_at = models.TimeField(default=timezone.now)

    def __str__(self) -> str:
        return self.title


class UserBox(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    box = models.ForeignKey(Box, on_delete=models.CASCADE)
    is_available = models.BooleanField(default=True)
    created_at = models.TimeField(default=timezone.now)

    def __str__(self) -> str:
        return f"UserBox of User {self.user}"


class Operation(models.Model):
    id = models.AutoField(primary_key=True)
    sum = models.IntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    box = models.ForeignKey(Box, on_delete=models.CASCADE)
    transaction_type = models.CharField(max_length=50)
    created_at = models.TimeField(default=timezone.now)

    def __str__(self) -> str:
        return f"Operation of user {self.user}"


class UserBalance(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    coin = models.ForeignKey(Coin, on_delete=models.CASCADE)
    balance = models.IntegerField()
    created_at = models.TimeField(default=timezone.now)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "coin"], name="unique_user_coin_balance"
            )
        ]

    def __str__(self) -> str:
        return f"Balance of user {self.user}"


class Notification(models.Model):
    id = models.AutoField(primary_key=True)
    action = models.CharField(max_length=50)
    text = models.CharField(max_length=50)
    created_at = models.TimeField(default=timezone.now)

    def __str__(self) -> str:
        return self.action


class UserNotification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE)
    created_at = models.TimeField(default=timezone.now)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "notification", "created_at"],
                name="unique_user_notification",
            )
        ]

    def __str__(self) -> str:
        return f"Notification of User {self.user}"
