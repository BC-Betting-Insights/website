# Generated by Django 2.1.5 on 2019-01-20 19:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leagues', '0003_league_currentmatchday'),
    ]

    operations = [
        migrations.AddField(
            model_name='league',
            name='count',
            field=models.IntegerField(null=True),
        ),
    ]