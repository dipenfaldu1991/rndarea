# Generated by Django 2.2.8 on 2020-06-26 11:18

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rnd_projects', '0006_auto_20200625_1012'),
    ]

    operations = [
        migrations.AddField(
            model_name='answer',
            name='reply',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='replies', to='rnd_projects.Answer'),
        ),
    ]
