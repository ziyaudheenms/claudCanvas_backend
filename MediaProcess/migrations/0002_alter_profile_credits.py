# Generated by Django 5.0 on 2025-05-02 11:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MediaProcess', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='credits',
            field=models.IntegerField(default=10),
        ),
    ]
