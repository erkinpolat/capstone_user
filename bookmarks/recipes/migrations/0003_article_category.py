# Generated by Django 3.0.11 on 2020-12-08 20:24

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('recipes', '0002_auto_20201205_1903'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('slug', models.SlugField(blank=True, max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('slug', models.SlugField(blank=True, max_length=200)),
                ('picture', models.ImageField(blank=True, upload_to='recipes/%Y/%m/%d/')),
                ('description', ckeditor.fields.RichTextField()),
                ('created', models.DateField(auto_now_add=True, db_index=True)),
                ('category', models.ForeignKey(on_delete=models.SET('Other'), related_name='articles_in_category', to='recipes.Category')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='articles_created', to=settings.AUTH_USER_MODEL)),
                ('users_like', models.ManyToManyField(blank=True, related_name='articles_liked', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
