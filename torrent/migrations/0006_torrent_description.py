# Generated by Django 4.1.7 on 2023-05-08 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('torrent', '0005_rename_data_torrent_file'),
    ]

    operations = [
        migrations.AddField(
            model_name='torrent',
            name='description',
            field=models.TextField(default='', verbose_name='Description'),
            preserve_default=False,
        ),
    ]
