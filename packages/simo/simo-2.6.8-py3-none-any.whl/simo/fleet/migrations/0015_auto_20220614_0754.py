# Generated by Django 3.2.9 on 2022-06-14 07:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fleet', '0014_auto_20220614_0659'),
    ]

    operations = [
        migrations.RenameField(
            model_name='colonel',
            old_name='upgrade_available',
            new_name='major_upgrade_available',
        ),
        migrations.AddField(
            model_name='colonel',
            name='minor_upgrade_available',
            field=models.CharField(editable=False, max_length=50, null=True),
        ),
    ]
