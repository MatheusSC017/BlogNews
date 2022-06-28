# Generated by Django 4.0.4 on 2022-06-28 11:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Search',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description_search', models.TextField(max_length=300, verbose_name='descrição')),
                ('creation_date_search', models.DateTimeField(default=django.utils.timezone.now, verbose_name='data de criação')),
                ('edition_date_search', models.DateTimeField(default=django.utils.timezone.now, verbose_name='data de edição')),
                ('publication_date_search', models.DateTimeField(default=django.utils.timezone.now, verbose_name='data de publicação')),
                ('finish_date_search', models.DateTimeField(verbose_name='data de termino')),
                ('published_search', models.BooleanField(default=True, verbose_name='publicado')),
                ('user_search', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='usuário')),
            ],
        ),
        migrations.CreateModel(
            name='Option',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('response_option', models.TextField(max_length=300, verbose_name='opção')),
                ('vote_option', models.PositiveIntegerField(verbose_name='número de votos')),
                ('search_option', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='search.search', verbose_name='pesquisa')),
            ],
        ),
    ]
