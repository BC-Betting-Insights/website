# Generated by Django 2.1.4 on 2019-01-15 14:36

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0010_auto_20190115_1433'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='team',
            name='league_slug',
        ),
        migrations.RemoveField(
            model_name='team',
            name='slug',
        ),
    ]
