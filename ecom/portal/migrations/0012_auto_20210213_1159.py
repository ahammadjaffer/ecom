# Generated by Django 3.1.4 on 2021-02-13 06:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0011_products_subcategoryid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='phonenumber',
            field=models.CharField(blank=True, max_length=13, null=True),
        ),
    ]
