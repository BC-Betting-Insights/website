# Generated by Django 2.1.4 on 2019-01-16 16:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matches', '0005_auto_20190116_1412'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='matchday',
            field=models.IntegerField(null=True),
        ),
    ]
