# Generated by Django 5.0.3 on 2024-07-27 21:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('homesite', '0002_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='price',
        ),
        migrations.AddField(
            model_name='orderitem',
            name='price',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
