# Generated by Django 5.1.7 on 2025-04-08 02:46

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_alter_customuser_family'),
        ('families', '0002_remove_family_members'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='family',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='members', to='families.family'),
        ),
    ]
