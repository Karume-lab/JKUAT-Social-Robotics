# Generated by Django 5.0.7 on 2024-08-07 15:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('people', '0004_person_personal_website_link'),
    ]

    operations = [
        migrations.AlterField(
            model_name='person',
            name='personal_website_link',
            field=models.URLField(blank=True, null=True, verbose_name='Personal Website Link'),
        ),
    ]
