# Generated by Django 3.1 on 2020-09-01 10:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='JobChat',
            fields=[
                ('id_chat', models.SmallIntegerField(default=-1, primary_key=True, serialize=False, verbose_name='id_chat')),
            ],
        ),
        migrations.CreateModel(
            name='JobMessage',
            fields=[
                ('id', models.SmallIntegerField(default=-1, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('text', models.CharField(default='text', max_length=255, verbose_name='text')),
                ('status', models.CharField(default='unread', max_length=300)),
                ('chat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chat.jobchat')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sendersss', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='JobPrivateChat',
            fields=[
                ('jobchat_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='chat.jobchat')),
                ('participant1', models.ForeignKey(default='admin', on_delete=django.db.models.deletion.CASCADE, related_name='participant1234', to=settings.AUTH_USER_MODEL)),
                ('participant2', models.ForeignKey(default='admin', on_delete=django.db.models.deletion.CASCADE, related_name='participant234', to=settings.AUTH_USER_MODEL)),
            ],
            bases=('chat.jobchat',),
        ),
    ]
