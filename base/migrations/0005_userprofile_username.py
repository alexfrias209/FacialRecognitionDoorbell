# Generated by Django 4.1.7 on 2023-03-22 22:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0004_account_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='username',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
    ]
