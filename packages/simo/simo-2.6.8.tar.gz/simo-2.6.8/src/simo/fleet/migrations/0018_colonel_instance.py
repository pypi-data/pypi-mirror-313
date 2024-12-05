# Generated by Django 3.2.9 on 2023-10-06 07:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0018_auto_20231005_0622'),
        ('fleet', '0017_alter_colonel_secret'),
    ]

    operations = [
        migrations.AddField(
            model_name='colonel',
            name='instance',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='colonels', to='core.instance'),
        ),
    ]
