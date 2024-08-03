# Generated by Django 4.1.7 on 2023-03-22 23:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0005_userprofile_username'),
    ]

    operations = [
        migrations.CreateModel(
            name='MultipleImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='')),
                ('account', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='base.account')),
            ],
        ),
        migrations.DeleteModel(
            name='Photo',
        ),
    ]
