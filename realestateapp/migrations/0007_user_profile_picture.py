# Generated by Django 4.0.4 on 2023-04-13 15:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('realestateapp', '0006_user_age_user_gender_user_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='profile_picture',
            field=models.ImageField(blank=True, null=True, upload_to='profile/'),
        ),
    ]
