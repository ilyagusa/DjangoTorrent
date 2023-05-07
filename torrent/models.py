from django.db import models

# Create your models here.


class Torrent(models.Model):
    name = models.CharField("Name", max_length=200)
    type = models.CharField("Type", max_length=50)
    image = models.ImageField("Image")
    file = models.FileField("File")
    score = models.FloatField("Score")
    genres = models.TextField("Genres")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Торрент'
        verbose_name_plural = 'Торренты'