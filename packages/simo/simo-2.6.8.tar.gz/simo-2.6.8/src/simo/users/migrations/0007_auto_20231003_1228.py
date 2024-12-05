# Generated by Django 3.2.9 on 2023-10-03 12:28

from django.db import migrations, models
import django.db.models.deletion



class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_auto_20231003_0850'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='roles',
            field=models.ManyToManyField(to='users.PermissionsRole'),
        ),
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rolerz', to='users.permissionsrole'),
        ),
    ]
