# Generated by Django 2.1.2 on 2018-11-18 21:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booru', '0003_auto_20181118_1918'),
    ]

    operations = [
        migrations.AddField(
            model_name='historicalpost',
            name='media_type',
            field=models.IntegerField(choices=[(0, 'Image'), (1, 'Video')], default=0),
        ),
        migrations.AddField(
            model_name='post',
            name='media_type',
            field=models.IntegerField(choices=[(0, 'Image'), (1, 'Video')], default=0),
        ),
    ]