# Generated by Django 5.0.7 on 2024-08-22 06:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_merge_20240822_0954'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basemodel',
            name='title',
            field=models.CharField(max_length=200, unique=True, verbose_name='Title'),
        ),
    ]