# Generated by Django 4.0.4 on 2022-05-21 12:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vid2text', '0002_videouploader'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Document',
        ),
    ]