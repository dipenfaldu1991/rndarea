# Generated by Django 2.2.8 on 2020-08-06 04:24

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
            name='AddPostdatas',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_name', models.CharField(max_length=200)),
                ('Category', models.CharField(max_length=200)),
                ('Location', models.CharField(max_length=200)),
                ('your_estimated_budget_minimum', models.CharField(max_length=200)),
                ('your_estimated_budget_maximum', models.CharField(max_length=200)),
                ('skills_are_required', models.CharField(max_length=200)),
                ('Describe_Your_Post', models.TextField(max_length=20000)),
                ('upload_file', models.FileField(upload_to='proje/')),
                ('date_posted', models.DateTimeField(auto_now_add=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
                ('created_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='createdaddostsuser', to=settings.AUTH_USER_MODEL)),
                ('updated_user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='updataddpostuser', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='BidCount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number_of_bid', models.IntegerField()),
                ('user_id', models.IntegerField(unique=True)),
                ('created_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Plans',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plan_name', models.CharField(max_length=100)),
                ('Description', models.TextField(max_length=2000)),
                ('price', models.IntegerField()),
                ('bid', models.IntegerField()),
                ('features1', models.CharField(max_length=500)),
                ('features2', models.CharField(max_length=500)),
                ('othersfeatures3', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('money', models.DecimalField(decimal_places=15, default=0, max_digits=30)),
                ('t_p_q_id', models.CharField(max_length=100)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
                ('created_user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cu', to=settings.AUTH_USER_MODEL)),
                ('updated_user', models.OneToOneField(null='True', on_delete=django.db.models.deletion.CASCADE, related_name='ur', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Questions',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=10000)),
                ('description', models.CharField(max_length=10000)),
                ('technology', models.CharField(max_length=1000)),
                ('skill', models.CharField(max_length=1000)),
                ('screenshort', models.FileField(upload_to='proje/')),
                ('date_posted', models.DateTimeField(auto_now_add=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
                ('created_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='createquestionsuser', to=settings.AUTH_USER_MODEL)),
                ('updated_user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='updatquestionsuser', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Projects_add_documents',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('project_icon', models.FileField(upload_to='proje/')),
                ('project_banner', models.FileField(upload_to='proje/')),
                ('documentation', models.FileField(upload_to='proje/')),
                ('intraction_document', models.FileField(upload_to='proje/')),
                ('other_reports', models.FileField(upload_to='proje/')),
                ('upload_video', models.FileField(upload_to='proje/')),
                ('screenshort_1', models.FileField(upload_to='proje/')),
                ('screenshort_2', models.FileField(upload_to='proje/')),
                ('screenshort_3', models.FileField(upload_to='proje/')),
                ('screenshort_4', models.FileField(upload_to='proje/')),
                ('screenshort_5', models.FileField(upload_to='proje/')),
                ('screenshort_6', models.FileField(upload_to='proje/')),
                ('zip_file', models.FileField(blank=True, null=True, upload_to='proje/')),
                ('project_add', models.PositiveIntegerField()),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
                ('deleted', models.DateTimeField(auto_now=True, null=True)),
                ('created_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='createdocumentsuser', to=settings.AUTH_USER_MODEL)),
                ('deleted_user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='deletedocumentsuser', to=settings.AUTH_USER_MODEL)),
                ('updated_user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='updatedocumentsuser', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Projects_add',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('headline', models.CharField(max_length=100)),
                ('Description', models.TextField(max_length=1000)),
                ('Technology', models.CharField(max_length=500)),
                ('Documents', models.CharField(max_length=100)),
                ('duration', models.CharField(max_length=100)),
                ('Relevant_Project', models.CharField(max_length=100)),
                ('Support', models.CharField(max_length=100)),
                ('Cost', models.DecimalField(decimal_places=15, max_digits=30)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated_user', models.PositiveIntegerField(blank=True, null=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
                ('deleted_user', models.PositiveIntegerField(blank=True, null=True)),
                ('deleted', models.DateTimeField(auto_now=True, null=True)),
                ('created_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='createuser', to=settings.AUTH_USER_MODEL)),
            ],
        ),
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
        migrations.CreateModel(
            name='Bidding',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bid_price', models.IntegerField()),
                ('create_bid_time', models.DateTimeField(auto_now_add=True, null=True)),
                ('bid_type', models.CharField(max_length=200)),
                ('delivery_time', models.IntegerField()),
                ('update_time', models.DateTimeField(null=True)),
                ('bid_user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='biduser', to=settings.AUTH_USER_MODEL)),
                ('task_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bid_task_id', to='rnd_projects.AddPostdatas')),
            ],
        ),
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answer', models.CharField(max_length=500000)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True, null=True)),
                ('created_user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='createuserid', to=settings.AUTH_USER_MODEL)),
                ('likes', models.ManyToManyField(blank=True, related_name='comment_likes', to=settings.AUTH_USER_MODEL)),
                ('parent', models.ForeignKey(blank='True', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='parentsss', to='rnd_projects.Answer')),
                ('question_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='createquestionsid', to='rnd_projects.Questions')),
                ('question_user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='createquestionsuserid', to=settings.AUTH_USER_MODEL)),
                ('updated_user', models.OneToOneField(null='True', on_delete=django.db.models.deletion.CASCADE, related_name='updateuser', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created'],
            },
        ),
    ]
