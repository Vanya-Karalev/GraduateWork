from django.db import models
from users.models import CustomUser


class Genre(models.Model):
    name = models.CharField(db_column='Name')

    class Meta:
        db_table = 'Genre'

    def __str__(self):
        return self.name


class Film(models.Model):
    genres = models.ManyToManyField(Genre)
    title = models.CharField(db_column='Title')
    eng_title = models.CharField(db_column='English title', default="")
    rating = models.FloatField(db_column='Rating', default=9.6)
    slogan = models.TextField(db_column='Slogan', default="")
    age = models.PositiveIntegerField(db_column='Age', default=18)
    description = models.TextField(db_column='Description')
    poster = models.URLField(db_column='Poster')
    trailer = models.URLField(db_column='Trailer')
    date = models.DateField(db_column='Date')
    country = models.CharField(db_column='Country')
    duration = models.PositiveIntegerField(db_column='Duration')
    slug = models.SlugField(null=False, unique=True, default="")

    class Meta:
        db_table = 'Film'

    def __str__(self):
        return self.title


class Room(models.Model):
    room_name = models.CharField(db_column='Room name')
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, db_column='OwnerID')
    # film
    # timer

    def __str__(self):
        return self.room_name


class Message(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE, db_column='SenderID')
    message = models.TextField()

    def __str(self):
        return str(self.room)


# class RoomUsers(models.Model):
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, db_column='UserID')
#
#     class Meta:
#         db_table = 'RoomUsers'
#
#     def __str__(self):
#         return str(self.pk)
