# Generated by Django 3.2.3 on 2021-06-30 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0015_auto_20210622_1601'),
    ]

    operations = [
        migrations.AlterField(
            model_name='warehouse',
            name='short_name',
            field=models.CharField(default='YP', max_length=10),
        ),
    ]
