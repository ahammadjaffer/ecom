# Generated by Django 3.1.4 on 2021-05-04 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0020_auto_20210504_2118'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='country',
            field=models.TextField(blank=True, max_length=500, null=True),
        ),
        migrations.AddField(
            model_name='profile',
            name='state',
            field=models.TextField(blank=True, max_length=500, null=True),
        ),
    ]
