# Generated by Django 2.0.3 on 2018-03-17 13:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Genre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
            ],
        ),
        migrations.CreateModel(
            name='Movie',
            fields=[
                ('movie_id', models.IntegerField(primary_key=True, serialize=False)),
                ('imdb_id', models.CharField(blank=True, max_length=30)),
                ('tmdb_id', models.CharField(blank=True, max_length=30)),
                ('title', models.CharField(max_length=30)),
                ('genres', models.ManyToManyField(related_name='movies', related_query_name='movie', to='main.Genre')),
            ],
        ),
        migrations.CreateModel(
            name='Rating',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.FloatField()),
                ('timestamp', models.DateTimeField()),
                ('movie', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='rating', to='main.Movie')),
            ],
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(max_length=100)),
                ('timestamp', models.DateTimeField()),
                ('movie', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='movie', to='main.Movie')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.IntegerField(primary_key=True, serialize=False)),
                ('movies', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user', to='main.Movie')),
            ],
        ),
        migrations.AddField(
            model_name='tag',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user', to='main.User'),
        ),
        migrations.AddField(
            model_name='rating',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='rating', to='main.User'),
        ),
    ]
