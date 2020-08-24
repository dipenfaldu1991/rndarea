# Generated by Django 3.1 on 2020-08-24 19:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('jobs', '0004_applynow'),
    ]

    operations = [
        migrations.CreateModel(
            name='jobsBookmark',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
                ('created_user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ggg', to=settings.AUTH_USER_MODEL)),
                ('jobid', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fg', to='jobs.addjobs')),
                ('updated_user', models.OneToOneField(null='True', on_delete=django.db.models.deletion.CASCADE, related_name='ffff', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
