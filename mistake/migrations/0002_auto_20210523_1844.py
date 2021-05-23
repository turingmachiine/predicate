# Generated by Django 3.2.2 on 2021-05-23 18:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('mistake', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mistake',
            name='changed_by_user',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='sentence',
            name='author',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]