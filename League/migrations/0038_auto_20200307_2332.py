# Generated by Django 2.1.7 on 2020-03-07 20:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('League', '0037_auto_20200307_2327'),
    ]

    operations = [
        migrations.AlterField(
            model_name='season',
            name='picture',
            field=models.ImageField(default='documents/vrlogo.png', null=True, upload_to='season_pics/%Y/%m/%d/'),
        ),
    ]
