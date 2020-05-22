# Generated by Django 2.1.7 on 2020-02-26 16:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('League', '0008_auto_20200226_1917'),
    ]

    operations = [
        migrations.AlterField(
            model_name='playlist',
            name='songs',
            field=models.ManyToManyField(limit_choices_to={'available_in': models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='League.Game')}, related_name='song_key', to='League.Song'),
        ),
    ]
