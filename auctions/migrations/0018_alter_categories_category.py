# Generated by Django 3.2.3 on 2021-07-01 22:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0017_auto_20210701_1628'),
    ]

    operations = [
        migrations.AlterField(
            model_name='categories',
            name='category',
            field=models.CharField(default='No Category', max_length=150),
        ),
    ]
