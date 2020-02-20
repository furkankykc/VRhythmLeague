# Generated by Django 2.1.7 on 2020-02-17 22:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('League', '0002_score'),
    ]

    operations = [
        migrations.AddField(
            model_name='score',
            name='score',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='score',
            name='player',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
