# Generated by Django 2.0.3 on 2018-03-19 22:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0005_auto_20180319_0647'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='ratings',
        ),
        migrations.RemoveField(
            model_name='user',
            name='ratings',
        ),
        migrations.AddField(
            model_name='rating',
            name='movie',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.Movie'),
        ),
        migrations.AddField(
            model_name='rating',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='main.User'),
        ),
    ]
