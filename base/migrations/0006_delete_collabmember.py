# Generated by Django 4.1.7 on 2023-04-28 00:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_remove_event_sentmail_mail'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CollabMember',
        ),
    ]
