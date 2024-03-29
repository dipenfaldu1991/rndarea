# Generated by Django 3.1 on 2020-08-14 11:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Chat',
            fields=[
                ('id_chat', models.SmallIntegerField(default=-1, primary_key=True, serialize=False, verbose_name='id_chat')),
            ],
        ),
        migrations.CreateModel(
            name='Warning',
            fields=[
                ('id', models.SmallIntegerField(default=-1, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('warning', models.CharField(default='text', max_length=255, verbose_name='warning')),
                ('status', models.CharField(default='unread', max_length=300)),
                ('chat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chat.chat')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='senders', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.SmallIntegerField(default=-1, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('text', models.CharField(default='text', max_length=255, verbose_name='text')),
                ('status', models.CharField(default='unread', max_length=300)),
                ('chat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='chat.chat')),
                ('sender', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sender', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PrivateChat',
            fields=[
                ('chat_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='chat.chat')),
                ('participant1', models.ForeignKey(default='admin', on_delete=django.db.models.deletion.CASCADE, related_name='participant1', to=settings.AUTH_USER_MODEL)),
                ('participant2', models.ForeignKey(default='admin', on_delete=django.db.models.deletion.CASCADE, related_name='participant2', to=settings.AUTH_USER_MODEL)),
            ],
            bases=('chat.chat',),
        ),
    ]
