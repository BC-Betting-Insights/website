# Generated by Django 2.1.5 on 2019-01-22 10:17

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leagues', '0004_league_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='league',
            name='list_date',
            field=models.DateTimeField(default=datetime.datetime.now),
        ),
    ]
