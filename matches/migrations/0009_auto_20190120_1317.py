# Generated by Django 2.1.5 on 2019-01-20 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matches', '0008_auto_20190118_1536'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='away_goals_sh',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='match',
            name='home_goals_sh',
            field=models.IntegerField(null=True),
        ),
    ]