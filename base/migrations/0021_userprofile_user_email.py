# Generated by Django 4.1.7 on 2023-04-01 07:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0020_userprofile_unique_string'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='user_email',
            field=models.EmailField(blank=True, max_length=200, null=True),
        ),
    ]
