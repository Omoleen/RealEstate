# Generated by Django 4.0.4 on 2023-03-12 21:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('realestateapp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='apartment',
            name='permalink',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
