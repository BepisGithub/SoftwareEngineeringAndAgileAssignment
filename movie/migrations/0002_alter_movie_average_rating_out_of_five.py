# Generated by Django 4.2.5 on 2023-09-06 16:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movie', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='average_rating_out_of_five',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
