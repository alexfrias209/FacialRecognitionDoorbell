# Generated by Django 4.1.7 on 2023-03-29 09:39

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0017_alter_phonenumber_phone_number'),
    ]

    operations = [
        migrations.AlterField(
            model_name='phonenumber',
            name='phone_number',
            field=phonenumber_field.modelfields.PhoneNumberField(default='+1', max_length=128, region=None),
        ),
    ]
