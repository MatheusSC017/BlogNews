# Generated by Django 4.0.4 on 2024-01-28 13:28

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
            name='Option',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('response', models.CharField(max_length=300, verbose_name='opção')),
            ],
            options={
                'verbose_name': 'alternativa',
            },
        ),
        migrations.CreateModel(
            name='VottingUserOption',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('option', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='search.option', verbose_name='alternativa')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='usuário')),
            ],
            options={
                'verbose_name': 'voto',
            },
        ),
        migrations.CreateModel(
            name='Search',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(max_length=300, verbose_name='descrição')),
                ('creation_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='data de criação')),
                ('edition_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='data de edição')),
                ('publication_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='data de publicação')),
                ('finish_date', models.DateTimeField(verbose_name='data de termino')),
                ('published', models.BooleanField(default=True, verbose_name='publicado')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='usuário')),
            ],
            options={
                'verbose_name': 'pesquisa',
            },
        ),
        migrations.AddField(
            model_name='option',
            name='search',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='search.search', verbose_name='pesquisa'),
        ),
        migrations.AddConstraint(
            model_name='vottinguseroption',
            constraint=models.UniqueConstraint(fields=('user', 'option'), name='user_option_vote'),
        ),
    ]
