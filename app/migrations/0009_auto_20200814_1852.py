# Generated by Django 2.2 on 2020-08-14 10:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_auto_20200802_2102'),
    ]

    operations = [
        migrations.AddField(
            model_name='compound',
            name='level',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='pdb',
            name='level',
            field=models.IntegerField(null=True),
        ),
    ]