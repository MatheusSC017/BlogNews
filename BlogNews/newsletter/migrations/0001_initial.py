# Generated by Django 4.0.4 on 2024-01-28 13:27

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='NewsLetterMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=998, verbose_name='título')),
                ('message', models.TextField(verbose_name='mensagem')),
                ('creation_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='data de criação')),
                ('edition_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='última edição')),
                ('published', models.BooleanField(default=False, verbose_name='publicado')),
            ],
            options={
                'verbose_name': 'mensagem',
                'verbose_name_plural': 'mensagens',
            },
        ),
        migrations.CreateModel(
            name='NewsLetterUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='e-mail')),
                ('creation_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='data de criação')),
                ('activated_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='data de ativação')),
                ('activated', models.BooleanField(default=True, verbose_name='ativado')),
            ],
            options={
                'verbose_name': 'usuário',
            },
        ),
    ]
