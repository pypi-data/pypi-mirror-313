# Generated by Django 4.2.10 on 2024-11-20 10:28

from django.db import migrations


def forwards_func(apps, schema_editor):
    Component = apps.get_model("core", "Component")

    for gate in Component.objects.filter(
        controller_uid='simo.fleet.controllers.Gate'
    ):
        gate.config['open_pin_no'] = gate.config.get('control_pin_no')
        gate.config['open_pin'] = gate.config.get('control_pin')
        gate.save()


def reverse_func(apps, schema_editor):
    pass



class Migration(migrations.Migration):

    dependencies = [
        ('fleet', '0041_alter_colonel_instance_and_more'),
    ]

    operations = [
        migrations.RunPython(forwards_func, reverse_func, elidable=True),
    ]
