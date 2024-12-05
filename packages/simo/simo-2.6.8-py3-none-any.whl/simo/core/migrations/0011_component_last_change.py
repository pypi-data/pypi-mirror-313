# Generated by Django 3.2.9 on 2023-10-02 06:38

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_historyaggregate'),
    ]

    operations = [
        migrations.AddField(
            model_name='component',
            name='last_change',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False, null=True),
        ),
    ]
