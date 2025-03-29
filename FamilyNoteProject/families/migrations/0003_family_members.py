# Generated by Django 5.1.7 on 2025-03-29 11:48

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('families', '0002_rename_name_family_family_name_family_created_at'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='family',
            name='members',
            field=models.ManyToManyField(related_name='families', to=settings.AUTH_USER_MODEL),
        ),
    ]
