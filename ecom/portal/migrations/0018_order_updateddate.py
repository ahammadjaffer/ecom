# Generated by Django 3.1.4 on 2021-03-27 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0017_auto_20210317_2126'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='updateddate',
            field=models.DateTimeField(null=True),
        ),
    ]