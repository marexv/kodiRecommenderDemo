# Generated by Django 2.0.3 on 2018-03-18 19:04

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_auto_20180318_1840'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rating',
            name='timestamp',
        ),
        migrations.RemoveField(
            model_name='tag',
            name='timestamp',
        ),
    ]
