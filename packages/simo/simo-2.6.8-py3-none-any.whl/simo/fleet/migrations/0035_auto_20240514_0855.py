# Generated by Django 3.2.9 on 2024-05-14 08:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        ('fleet', '0034_auto_20240418_0735'),
    ]

    operations = [
        migrations.CreateModel(
            name='InterfaceAddress',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address_type', models.CharField(choices=[('i2c', 'I2C'), ('dali-gear', 'DALI Gear'), ('dali-group', 'DALI Gear Group')], db_index=True, max_length=100)),
                ('address', models.JSONField(db_index=True)),
                ('occupied_by_id', models.PositiveIntegerField(null=True)),
                ('interface', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='addresses', to='fleet.interface')),
                ('occupied_by_content_type', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
            ],
            options={
                'unique_together': {('interface', 'address_type', 'address')},
            },
        ),
        migrations.DeleteModel(
            name='I2CInterface',
        ),
    ]
