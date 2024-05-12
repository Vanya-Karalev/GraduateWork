from django.db import models


class Genre(models.Model):
    name = models.CharField(db_column='Name')

    class Meta:
        db_table = 'Genre'

    def __str__(self):
        return self.name


class Film(models.Model):
    genres = models.ManyToManyField(Genre)
    title = models.CharField(db_column='Title')
    description = models.TextField(db_column='Description')
    poster = models.URLField(db_column='Poster')
    trailer = models.URLField(db_column='Trailer')
    date = models.DateField(db_column='Date')
    country = models.CharField(db_column='Country')
    duration = models.PositiveIntegerField(db_column='Duration')

    class Meta:
        db_table = 'Film'

    def __str__(self):
        return self.title
