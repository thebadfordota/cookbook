# Generated by Django 3.2.4 on 2021-06-24 08:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ingredients',
            options={'ordering': ['-name'], 'verbose_name': 'ингредиент', 'verbose_name_plural': 'ингредиенты'},
        ),
    ]
