# Generated by Django 4.2 on 2023-04-27 04:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0030_userprofile_embeddings'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='embeddings',
        ),
        migrations.AddField(
            model_name='userprofile',
            name='data_file',
            field=models.FileField(blank=True, null=True, upload_to='data_files/'),
        ),
    ]