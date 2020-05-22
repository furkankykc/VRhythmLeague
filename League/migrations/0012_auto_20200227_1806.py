# Generated by Django 2.1.7 on 2020-02-27 15:06

from django.db import migrations
import django.db.models.deletion
import smart_selects.db_fields


class Migration(migrations.Migration):

    dependencies = [
        ('League', '0011_auto_20200226_1948'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='playlist',
            name='songs',
        ),
        migrations.AddField(
            model_name='playlist',
            name='songs',
            field=smart_selects.db_fields.GroupedForeignKey(default=1, group_field='game', on_delete=django.db.models.deletion.CASCADE, to='League.Song'),
            preserve_default=False,
        ),
    ]
