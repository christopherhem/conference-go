# Generated by Django 4.0.3 on 2022-08-25 00:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendees', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='accountvo',
            name='email',
            field=models.EmailField(max_length=100, null=True),
        ),
    ]
