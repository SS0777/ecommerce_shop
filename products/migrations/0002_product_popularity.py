# Generated by Django 5.1.4 on 2024-12-26 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='popularity',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
