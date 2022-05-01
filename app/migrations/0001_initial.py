# Generated by Django 2.2 on 2020-07-01 17:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='compound',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('uniprotKB', models.CharField(max_length=20, null=True)),
                ('gene', models.CharField(max_length=20, null=True)),
                ('InChl', models.CharField(max_length=500, null=True)),
                ('InChlKey', models.CharField(max_length=500, null=True)),
                ('MolecularFormula', models.CharField(max_length=100, null=True)),
                ('MolecularWeight', models.CharField(max_length=20, null=True)),
                ('smiles', models.CharField(max_length=500, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='gene',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('go', models.CharField(max_length=20, null=True)),
                ('goterm', models.CharField(max_length=20, null=True)),
                ('protein', models.CharField(max_length=500, null=True)),
                ('gene', models.CharField(max_length=500, null=True)),
                ('synonyms', models.CharField(max_length=100, null=True)),
                ('uniprotKB', models.CharField(max_length=20, null=True)),
            ],
        ),
    ]