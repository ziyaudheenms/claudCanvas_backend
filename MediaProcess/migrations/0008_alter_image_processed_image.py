# Generated by Django 5.0 on 2025-05-09 13:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MediaProcess', '0007_alter_video_transformed_video_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='processed_image',
            field=models.CharField(default='one', max_length=225),
            preserve_default=False,
        ),
    ]
