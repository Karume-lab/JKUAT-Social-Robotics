# Generated by Django 5.0.7 on 2024-08-08 12:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_alter_basemodel_cover_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basemodel',
            name='title',
            field=models.CharField(max_length=50, unique=True, verbose_name='Title'),
        ),
    ]