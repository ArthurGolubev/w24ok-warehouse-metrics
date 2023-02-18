# Generated by Django 3.2.3 on 2021-05-27 05:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Organizer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Username',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Warehouse',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cod', models.CharField(max_length=50)),
                ('datetime', models.DateTimeField()),
                ('target', models.CharField(max_length=20)),
                ('purchase_title', models.CharField(max_length=500)),
                ('transport_charges', models.IntegerField()),
                ('paid', models.IntegerField()),
                ('paid_by_card', models.BooleanField(default=False)),
                ('fine', models.IntegerField()),
                ('org', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.organizer')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.username')),
            ],
        ),
    ]
