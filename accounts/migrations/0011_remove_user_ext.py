# Generated by Django 4.1.3 on 2022-12-23 05:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0010_user_ext'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='ext',
        ),
    ]
