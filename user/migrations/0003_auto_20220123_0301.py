# Generated by Django 3.0.7 on 2022-01-22 21:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0002_userdata_user_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userdata',
            name='user_pic',
            field=models.ImageField(blank=True, upload_to='images'),
        ),
    ]