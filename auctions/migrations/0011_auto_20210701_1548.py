# Generated by Django 3.2.3 on 2021-07-01 21:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0010_alter_listing_postdate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='Image',
            field=models.ImageField(blank=True, default='https://icdn.football-espana.net/wp-content/uploads/2020/11/2b34dac481e247c97f0aa12902505c90.jpg', upload_to=''),
        ),
        migrations.AlterField(
            model_name='listing',
            name='PostDate',
            field=models.DateTimeField(default='%d- %m - %y, %h:%m:%s'),
        ),
    ]
