# Generated by Django 2.0.2 on 2018-06-21 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0008_product_redirect_count'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='redirect_count',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
