# Generated by Django 3.2.3 on 2021-07-12 19:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0024_auto_20210712_0305'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='Active',
            field=models.BooleanField(default=True),
        ),
    ]