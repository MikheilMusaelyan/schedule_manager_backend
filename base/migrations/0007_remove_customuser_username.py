# Generated by Django 4.1.7 on 2023-04-28 02:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0006_delete_collabmember'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='username',
        ),
    ]