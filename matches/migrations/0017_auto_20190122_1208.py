# Generated by Django 2.1.5 on 2019-01-22 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matches', '0016_auto_20190120_1753'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='match',
            name='matchday',
        ),
        migrations.AddField(
            model_name='match',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='match',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
