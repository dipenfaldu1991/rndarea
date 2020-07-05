# Generated by Django 2.2.8 on 2020-07-05 13:45

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('rnd_projects', '0006_auto_20200702_1525'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectOrder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plan_price', models.FloatField()),
                ('gst', models.FloatField()),
                ('total', models.FloatField()),
                ('created_orde_time', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(default='pending', max_length=300)),
                ('plan_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_user_id', to='rnd_projects.Plans')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='projectorder_user_id', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='PaymentDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('payment_id', models.CharField(max_length=100)),
                ('amount', models.FloatField()),
                ('gst', models.FloatField()),
                ('total', models.FloatField()),
                ('payment_date', models.DateTimeField(auto_now_add=True)),
                ('order_id', models.IntegerField()),
                ('status', models.CharField(max_length=300)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('back_name', models.CharField(max_length=200)),
                ('back_txnid', models.CharField(max_length=200)),
                ('payment_mode', models.CharField(max_length=200)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='payment_user_id', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plan_price', models.FloatField()),
                ('gst', models.FloatField()),
                ('total', models.FloatField()),
                ('created_orde_time', models.DateTimeField(auto_now_add=True)),
                ('status', models.CharField(default='pending', max_length=300)),
                ('plan_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='plan_user_id', to='rnd_projects.Plans')),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_user_id', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
