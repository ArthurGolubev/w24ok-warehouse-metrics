# Generated by Django 3.2.3 on 2021-06-18 04:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_prolongation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='cod',
            field=models.CharField(max_length=150, unique_for_date='datetime'),
        ),
    ]