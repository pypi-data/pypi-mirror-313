# Generated by Django 2.2.12 on 2021-09-24 11:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime', models.DateTimeField(auto_now_add=True)),
                ('severity', models.CharField(choices=[('info', 'Info'), ('warning', 'Warning'), ('alarm', 'Alarm')], db_index=True, max_length=100)),
                ('title', models.CharField(max_length=500)),
                ('body', models.TextField(blank=True, null=True)),
                ('component', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='core.Component')),
            ],
        ),
        migrations.CreateModel(
            name='UserNotification',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sent', models.DateTimeField(blank=True, db_index=True, null=True)),
                ('archived', models.DateTimeField(blank=True, db_index=True, null=True)),
                ('notification', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_notifications', to='notifications.Notification')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='notification',
            name='to_users',
            field=models.ManyToManyField(through='notifications.UserNotification', to=settings.AUTH_USER_MODEL),
        ),
    ]
