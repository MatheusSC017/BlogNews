# Generated by Django 4.0.4 on 2022-06-30 19:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0002_alter_option_options_alter_search_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='option',
            name='response_option',
            field=models.CharField(max_length=300, verbose_name='opção'),
        ),
    ]
