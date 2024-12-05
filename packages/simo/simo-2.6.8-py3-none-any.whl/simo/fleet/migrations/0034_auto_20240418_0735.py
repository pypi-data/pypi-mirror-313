# Generated by Django 3.2.9 on 2024-04-18 07:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('fleet', '0033_auto_20240415_0736'),
    ]

    operations = [
        migrations.AlterField(
            model_name='interface',
            name='pin_a',
            field=models.ForeignKey(editable=False, limit_choices_to={'native': True, 'output': True}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='interface_a', to='fleet.colonelpin', verbose_name='Pin A (scl)'),
        ),
        migrations.AlterField(
            model_name='interface',
            name='pin_b',
            field=models.ForeignKey(editable=False, limit_choices_to={'native': True, 'output': True}, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='interface_b', to='fleet.colonelpin', verbose_name='Pin B (sda)'),
        ),
    ]
