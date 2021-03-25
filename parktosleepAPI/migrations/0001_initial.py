# Generated by Django 3.1.7 on 2021-03-25 17:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='DaysOfTheWeek',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Rentee',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=50)),
                ('city', models.CharField(max_length=50)),
                ('state', models.CharField(max_length=50)),
                ('country', models.CharField(max_length=50)),
                ('phone', models.IntegerField()),
                ('pts_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='RentalPost',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('max_length', models.IntegerField()),
                ('description', models.CharField(max_length=350)),
                ('city', models.CharField(max_length=50)),
                ('state', models.CharField(max_length=50)),
                ('address', models.CharField(max_length=50)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('rentee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='parktosleepAPI.rentee')),
            ],
        ),
        migrations.CreateModel(
            name='DaysAvailable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('days', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='parktosleepAPI.daysoftheweek')),
                ('rental_post', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='parktosleepAPI.rentalpost')),
            ],
        ),
        migrations.CreateModel(
            name='BookedSpot',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField()),
                ('rental_spot', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='parktosleepAPI.rentalpost')),
                ('renter', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='parktosleepAPI.rentee')),
            ],
        ),
    ]
