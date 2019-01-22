# Generated by Django 2.1.4 on 2019-01-16 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matches', '0004_match_league_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='match',
            name='away_goals',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='match',
            name='away_goals_first_half',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='match',
            name='home_goals',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='match',
            name='home_goals_first_half',
            field=models.IntegerField(null=True),
        ),
    ]
