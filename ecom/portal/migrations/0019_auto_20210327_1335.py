# Generated by Django 3.1.4 on 2021-03-27 08:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0018_order_updateddate'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderdetails',
            name='status',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='orderdetails',
            name='updateddate',
            field=models.DateTimeField(null=True),
        ),
    ]
