# Generated by Django 3.2.9 on 2024-04-18 07:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0025_rename_name_fingerprint_type_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='fingerprint',
            name='name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
