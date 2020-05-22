# Generated by Django 2.1.7 on 2020-02-22 19:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('League', '0002_auto_20200222_0503'),
    ]

    operations = [
        migrations.RenameField(
            model_name='difficulty',
            old_name='max_score',
            new_name='bombs',
        ),
        migrations.RenameField(
            model_name='difficulty',
            old_name='stars',
            new_name='duration',
        ),
        migrations.RenameField(
            model_name='song',
            old_name='played_count',
            new_name='downloads',
        ),
        migrations.RemoveField(
            model_name='difficulty',
            name='name',
        ),
        migrations.RemoveField(
            model_name='difficulty',
            name='ranked',
        ),
        migrations.AddField(
            model_name='difficulty',
            name='length',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='difficulty',
            name='njs',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='difficulty',
            name='njs_offset',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='difficulty',
            name='notes',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='difficulty',
            name='obstacles',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='song',
            name='cover_url',
            field=models.URLField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='song',
            name='description',
            field=models.CharField(default=0, max_length=150),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='song',
            name='direct_download',
            field=models.URLField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='song',
            name='download_url',
            field=models.URLField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='song',
            name='plays',
            field=models.BigIntegerField(default=0),
            preserve_default=False,
        ),
    ]
