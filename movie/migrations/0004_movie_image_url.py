# Generated by Django 4.2.5 on 2023-09-17 18:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0003_alter_movie_average_rating_out_of_five'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='image_url',
            field=models.URLField(blank=True, max_length=500, null=True),
        ),
    ]