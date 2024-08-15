# Generated by Django 5.0.7 on 2024-08-13 13:59

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('core', '0004_alter_basemodel_title'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('basemodel_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='core.basemodel')),
                ('location', models.CharField(max_length=50, verbose_name='Location')),
                ('date_starting', models.DateTimeField(blank=True, null=True, verbose_name='Date Starting')),
                ('date_ending', models.DateTimeField(blank=True, null=True, verbose_name='Date Ending')),
            ],
            options={
                'verbose_name': 'News',
                'verbose_name_plural': 'News',
            },
            bases=('core.basemodel',),
        ),
    ]