# Generated by Django 3.2.3 on 2021-05-28 06:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_warehouse_short_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='warehouse',
            name='name',
            field=models.CharField(max_length=50, null=True),
        ),
    ]