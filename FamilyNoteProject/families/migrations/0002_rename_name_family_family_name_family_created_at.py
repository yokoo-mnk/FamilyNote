# Generated by Django 5.1.7 on 2025-03-29 10:15

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('families', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='family',
            old_name='name',
            new_name='family_name',
        ),
        migrations.AddField(
            model_name='family',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
