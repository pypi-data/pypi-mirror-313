# Generated by Django 4.2.10 on 2024-03-06 08:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('fleet', '0027_auto_20240306_0802'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='i2cinterface',
            name='scl_pin_no',
        ),
        migrations.RemoveField(
            model_name='i2cinterface',
            name='sda_pin_no',
        ),
    ]
