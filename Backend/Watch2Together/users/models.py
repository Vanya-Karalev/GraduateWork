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
