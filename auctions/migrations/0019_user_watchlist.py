# Generated by Django 3.2.3 on 2021-07-05 01:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0018_alter_categories_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='Watchlist',
            field=models.ManyToManyField(blank=True, to='auctions.Listing'),
        ),
    ]