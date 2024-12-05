# Generated by Django 4.2.10 on 2024-10-18 08:00

from django.db import migrations, models
import location_field.models.plain


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0033_alter_user_ssh_key'),
    ]

    operations = [
        migrations.AddField(
            model_name='instanceuser',
            name='last_seen_location',
            field=location_field.models.plain.PlainLocationField(blank=True, help_text='Sent by user mobile app', max_length=63, null=True),
        ),
        migrations.AddField(
            model_name='instanceuser',
            name='last_seen_location_datetime',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
