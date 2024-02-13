# Generated by Django 5.0.2 on 2024-02-12 16:34

import shortuuid.main
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='profile_image',
            field=models.ImageField(blank=True, default='profile/default.png', null=True, upload_to='profile/', verbose_name='Profile Image'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='id',
            field=models.CharField(default=shortuuid.main.ShortUUID.uuid, editable=False, max_length=22, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
