# Generated by Django 5.0.7 on 2024-08-13 04:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_basemodel_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='basemodel',
            name='title',
            field=models.CharField(max_length=100, unique=True, verbose_name='Title'),
        ),
    ]
