# Generated by Django 3.1.4 on 2021-09-20 15:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0021_auto_20210504_2135'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='paymentstatus',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
