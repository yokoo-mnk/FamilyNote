# Generated by Django 5.1.7 on 2025-04-08 00:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('families', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='family',
            name='members',
        ),
    ]
