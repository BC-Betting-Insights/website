# Generated by Django 2.1.4 on 2018-12-26 13:37

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('teams', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Match',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('home_goals', models.IntegerField()),
                ('away_goals', models.IntegerField()),
                ('home_goals_first_half', models.IntegerField()),
                ('away_goals_first_half', models.IntegerField()),
                ('home_possession', models.IntegerField()),
                ('home_shots_target', models.IntegerField()),
                ('away_shots_target', models.IntegerField()),
                ('is_played', models.BooleanField(default=True)),
                ('list_date', models.DateTimeField(default=datetime.datetime.now)),
                ('away_team', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='away_team', to='teams.Team')),
                ('home_team', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='home_team', to='teams.Team')),
            ],
        ),
    ]