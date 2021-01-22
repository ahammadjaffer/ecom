# Generated by Django 3.1.4 on 2021-01-02 16:03

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('addeddate', models.DateTimeField(auto_now=True)),
                ('enddate', models.DateTimeField(null=True)),
                ('status', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('description', models.CharField(max_length=1000)),
                ('categoryid', models.IntegerField()),
                ('count', models.IntegerField()),
                ('price', models.IntegerField()),
                ('tax', models.IntegerField()),
                ('sellerid', models.IntegerField()),
                ('addeddate', models.DateTimeField(auto_now=True)),
                ('enddate', models.DateTimeField(null=True)),
                ('status', models.IntegerField()),
                ('discount', models.IntegerField(null=True)),
                ('shipmentcharge', models.IntegerField()),
            ],
        ),
    ]
