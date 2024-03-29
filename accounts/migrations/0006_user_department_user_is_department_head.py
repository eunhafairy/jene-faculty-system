# Generated by Django 4.1.3 on 2022-12-18 05:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('department', '0001_initial'),
        ('accounts', '0005_alter_user_groups_alter_user_user_permissions'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='department',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='department', to='department.department'),
        ),
        migrations.AddField(
            model_name='user',
            name='is_department_head',
            field=models.BooleanField(default=False),
        ),
    ]
