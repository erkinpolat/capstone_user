# Generated by Django 3.0.11 on 2021-02-18 23:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_cookbook_created'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cookbook',
            name='created',
            field=models.DateField(auto_now_add=True, db_index=True),
        ),
    ]
