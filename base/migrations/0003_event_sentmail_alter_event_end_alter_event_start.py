# Generated by Django 4.1.7 on 2023-04-25 22:29

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0002_remove_customuser_age_remove_customuser_bio'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='sentMail',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='event',
            name='end',
            field=models.IntegerField(validators=[django.core.validators.MaxValueValidator(96), django.core.validators.MinValueValidator(1)]),
        ),
        migrations.AlterField(
            model_name='event',
            name='start',
            field=models.IntegerField(validators=[django.core.validators.MaxValueValidator(95), django.core.validators.MinValueValidator(0)]),
        ),
    ]