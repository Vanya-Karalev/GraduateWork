from django.db import models
from django.contrib.auth.models import AbstractUser


class Role(models.Model):
    name = models.CharField(db_column='Name')

    class Meta:
        db_table = 'Role'

    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
    role = models.ForeignKey(Role, models.CASCADE, db_column='RoleID', default=2)
    image = models.FileField(upload_to="images/", null=True)
    subscription = models.BooleanField(default=False, db_column='Subscription')
    period = models.IntegerField(default=0, db_column='Subscription period')


class Friends(models.Model):
    STATUS_CHOICES = (
        ('request_sent', 'Заявка отправлена'),
        ('friends', 'Друзья'),
    )
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, db_column='SenderID', related_name='sender')
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, db_column='ReceiverID', related_name='receiver')
    status = models.CharField(db_column='Status', choices=STATUS_CHOICES, default='request_declined')

    class Meta:
        db_table = 'Friends'

    def __str__(self):
        return self.status


class Notifications(models.Model):
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, db_column='SenderID', related_name='notification_sender')
    receiver = models.ForeignKey(CustomUser, on_delete=models.CASCADE, db_column='ReceiverID', related_name='notification_receiver')
    text_notification = models.TextField(db_column='Notification')

    class Meta:
        db_table = 'Notifications'

    def __str__(self):
        return self.text_notification
