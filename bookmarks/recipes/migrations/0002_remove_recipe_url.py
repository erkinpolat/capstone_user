# Generated by Django 3.0.11 on 2020-11-13 14:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipe',
            name='url',
        ),
    ]