# Generated by Django 2.2.8 on 2020-07-27 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rnd_projects', '0009_wallet'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wallet',
            name='money',
            field=models.DecimalField(decimal_places=15, default=0, max_digits=30),
        ),
    ]
