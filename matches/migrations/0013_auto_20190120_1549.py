# Generated by Django 2.1.5 on 2019-01-20 15:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('matches', '0012_auto_20190120_1437'),
    ]

    operations = [
        migrations.AddField(
            model_name='match',
            name='result',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='match',
            name='result_fh',
            field=models.CharField(max_length=200, null=True),
        ),
        migrations.AddField(
            model_name='match',
            name='result_sh',
            field=models.CharField(max_length=200, null=True),
        ),
    ]