# Generated by Django 5.0.7 on 2024-08-03 07:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('publications', '0002_remove_publication_cover_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='publication',
            name='document',
            field=models.FileField(blank=True, null=True, upload_to=None, verbose_name='Document'),
        ),
    ]
