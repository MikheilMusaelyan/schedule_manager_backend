# Generated by Django 3.2.19 on 2023-05-12 23:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0010_auto_20230512_1630'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='password',
            field=models.CharField(max_length=150),
        ),
    ]
