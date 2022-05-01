from django.db import models

# Create your models here.


class compound(models.Model):

    id = models.IntegerField(primary_key=True)
    uniprotKB = models.CharField(max_length=20, null=True)
    gene = models.CharField(max_length=20, null=True)
    InChI = models.CharField(max_length=500, null=True)
    InChIKey = models.CharField(max_length=500, null=True)
    MolecularFormula = models.CharField(max_length=100, null=True)
    MolecularWeight = models.CharField(max_length=20, null=True)
    smiles = models.CharField(max_length=500, null=True)
    prop = models.CharField(max_length=500, null=True)
    level = models.IntegerField(null=True)
    md5 = models.CharField(max_length=500, null=True)

    def __str__(self):
        return self.smiles


class gene(models.Model):

    id = models.IntegerField(primary_key=True)
    go = models.CharField(max_length=500, null=True)
    go0 = models.CharField(max_length=500, null=True)
    goterm = models.CharField(max_length=500, null=True)
    goterm0 = models.CharField(max_length=500, null=True)
    protein = models.CharField(max_length=500, null=True)
    gene = models.CharField(max_length=500, null=True)
    synonyms = models.CharField(max_length=100, null=True)
    uniprotKB = models.CharField(max_length=20, null=True)
    level = models.IntegerField(null=True)
    pmid = models.CharField(max_length=500, null=True)

    def __str__(self):
        return self.gene


class pdb(models.Model):

    id = models.IntegerField(primary_key=True)
    uniprot = models.CharField(max_length=500, null=True)
    gene = models.CharField(max_length=500, null=True)
    pdb = models.CharField(max_length=500, null=True)
    date = models.CharField(max_length=500, null=True)
    method = models.CharField(max_length=500, null=True)
    level = models.IntegerField(null=True)

    def __str__(self):
        return self.gene


class figc(models.Model):

    id = models.IntegerField(primary_key=True)
    gene = models.CharField(max_length=500, null=True)
    number = models.IntegerField(null=True)
    level = models.IntegerField(null=True)
    factor = models.FloatField(null=True)

    def __str__(self):
        return self.gene


class figd(models.Model):

    id = models.IntegerField(primary_key=True)
    gene = models.CharField(max_length=500, null=True)
    number = models.IntegerField(null=True)
    level = models.IntegerField(null=True)
    factor = models.FloatField(null=True)

    def __str__(self):
        return self.gene
