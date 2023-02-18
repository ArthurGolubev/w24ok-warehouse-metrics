# Generated by Django 3.2.3 on 2021-05-30 10:33

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_alter_warehouse_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='warehouse',
            name='datetime',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
