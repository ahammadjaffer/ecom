# Generated by Django 3.1.4 on 2021-02-15 10:26

import builtins
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('portal', '0014_auto_20210214_1305'),
    ]

    operations = [
        migrations.CreateModel(
            name='Companydetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('address', models.TextField(blank=True, max_length=500, null=True)),
                ('email', models.CharField(max_length=255)),
                ('phonenumber', models.CharField(max_length=13)),
                ('termsandconditions', models.TextField(blank=True, max_length=builtins.max, null=True)),
                ('facebook', models.CharField(max_length=255)),
                ('instagram', models.CharField(max_length=255)),
                ('youtube', models.CharField(max_length=255)),
            ],
        ),
        migrations.AlterField(
            model_name='banners',
            name='bannerimage',
            field=models.ImageField(blank=True, null=True, upload_to='images/'),
        ),
    ]
