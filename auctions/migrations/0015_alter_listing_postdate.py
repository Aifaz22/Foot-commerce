# Generated by Django 3.2.3 on 2021-07-01 22:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0014_alter_listing_postdate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='PostDate',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
