# Generated by Django 4.2 on 2023-04-26 22:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0022_delete_room_alter_userprofile_profile_picture'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserProfileImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('images', models.ImageField(upload_to='user_profile_images/')),
                ('user_profile', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.userprofile')),
            ],
        ),
    ]
