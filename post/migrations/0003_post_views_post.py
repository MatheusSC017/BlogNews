# Generated by Django 4.0.4 on 2022-06-06 11:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0002_alter_post_excerpt_post'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='views_post',
            field=models.PositiveIntegerField(default=0, verbose_name='Visualizações'),
        ),
    ]
