# Generated by Django 4.2.10 on 2024-11-18 09:32

from django.db import migrations, models
import location_field.models.plain


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0039_auto_20241117_1039'),
    ]

    operations = [
        migrations.AddField(
            model_name='userdevicereportlog',
            name='location_smoothed',
            field=location_field.models.plain.PlainLocationField(blank=True, max_length=63, null=True),
        ),
        migrations.AlterField(
            model_name='userdevicereportlog',
            name='at_home',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='userdevicereportlog',
            name='datetime',
            field=models.DateTimeField(auto_now_add=True, db_index=True),
        ),
    ]
