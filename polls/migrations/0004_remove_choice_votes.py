# Generated by Django 3.1.1 on 2020-11-01 13:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('polls', '0003_vote'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='choice',
            name='votes',
        ),
    ]
