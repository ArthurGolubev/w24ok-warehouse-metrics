# Generated by Django 3.2.3 on 2021-06-22 09:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_alter_transaction_cod'),
    ]

    operations = [
        migrations.AlterField(
            model_name='transaction',
            name='org',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.organizer'),
        ),
        migrations.AlterField(
            model_name='transaction',
            name='purchase_title',
            field=models.CharField(max_length=1000, null=True),
        ),
    ]
