# Generated by Django 2.1.5 on 2019-01-16 17:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('newsletters', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='NewsletterUsers',
            new_name='NewsletterUser',
        ),
    ]
