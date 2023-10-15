from django.db import models

# Create your models here.


class Torrent(models.Model):
    name = models.CharField("Name", max_length=200)

    type = models.CharField("Type", max_length=50)
    score = models.FloatField("Score")
    genres = models.TextField("Genres")
    description = models.TextField("Description")
    info = models.JSONField("Info")

    image = models.ImageField("Image")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Торрент'
        verbose_name_plural = 'Торренты'


class TorrentFile(models.Model):
    file = models.FileField("File")
    size = models.CharField("Size", max_length=20)
    file_format = models.CharField("Format", max_length=20)

    torrent = models.ForeignKey(Torrent, on_delete=models.CASCADE)
