# Generated by Django 3.2.3 on 2021-07-01 22:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0016_auto_20210701_1608'),
    ]

    operations = [
        migrations.CreateModel(
            name='Categories',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=150)),
            ],
        ),
        migrations.AlterField(
            model_name='listing',
            name='Category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auctions.categories'),
        ),
    ]
