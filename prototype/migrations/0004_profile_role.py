# Generated by Django 3.1.3 on 2020-11-20 14:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prototype', '0003_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='role',
            field=models.CharField(choices=[('STAFF', 'Staff'), ('CLIENT', 'Client')], default='CLIENT', max_length=10),
        ),
    ]
