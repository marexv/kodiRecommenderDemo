# Generated by Django 2.0.3 on 2018-03-19 06:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0004_auto_20180318_1904'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='ratings',
        ),
        migrations.AddField(
            model_name='movie',
            name='ratings',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='movies', related_query_name='movie', to='main.Rating'),
        ),
        migrations.RemoveField(
            model_name='user',
            name='ratings',
        ),
        migrations.AddField(
            model_name='user',
            name='ratings',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='users', related_query_name='user', to='main.Rating'),
        ),
    ]
