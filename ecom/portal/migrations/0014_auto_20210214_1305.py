# Generated by Django 3.1.4 on 2021-02-14 07:35

import django.core.files.storage
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0013_banners'),
    ]

    operations = [
        migrations.AlterField(
            model_name='banners',
            name='bannerimage',
            field=models.ImageField(blank=True, null=True, storage=django.core.files.storage.FileSystemStorage(location='/media/banners'), upload_to=''),
        ),
    ]
