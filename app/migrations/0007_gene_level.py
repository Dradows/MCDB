# Generated by Django 3.0.8 on 2020-08-02 20:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_compound_prop'),
    ]

    operations = [
        migrations.AddField(
            model_name='gene',
            name='level',
            field=models.IntegerField(null=True),
        ),
    ]
