# Generated by Django 3.2.6 on 2023-02-06 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='userSetRole',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]