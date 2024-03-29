# Generated by Django 4.1.3 on 2022-12-18 06:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('department', '0002_alter_department_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='department',
            name='head',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='department', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='department',
            name='code',
            field=models.CharField(max_length=10, unique=True),
        ),
    ]
