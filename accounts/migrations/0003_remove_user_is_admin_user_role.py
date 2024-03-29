# Generated by Django 4.1.3 on 2022-12-11 00:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_alter_user_options_alter_user_managers_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='is_admin',
        ),
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.SmallIntegerField(choices=[('1', 'Admin'), ('2', 'Research Coordinator'), ('3', 'Extension Coordinator'), ('4', 'Department Head'), ('5', 'Faculty')], default='5'),
        ),
    ]
