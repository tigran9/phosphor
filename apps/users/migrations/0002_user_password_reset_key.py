# Generated by Django 2.1.2 on 2018-10-16 12:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='password_reset_key',
            field=models.CharField(default=None, max_length=255, null=True),
        ),
    ]
