# Generated by Django 2.1.4 on 2019-01-15 14:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('teams', '0007_team_league_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='team',
            name='divslug',
        ),
        migrations.RemoveField(
            model_name='team',
            name='league_slug',
        ),
        migrations.RemoveField(
            model_name='team',
            name='slug',
        ),
    ]
