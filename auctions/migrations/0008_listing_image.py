# Generated by Django 3.2.3 on 2021-06-07 07:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0007_auto_20210606_2058'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='Image',
            field=models.ImageField(blank=True, default='https://icdn.football-espana.net/wp-content/uploads/2020/11/2b34dac481e247c97f0aa12902505c90.jpg', upload_to='users/%Y/%m/%d/'),
        ),
    ]
