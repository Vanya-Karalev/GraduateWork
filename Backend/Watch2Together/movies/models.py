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
