from openbabel.pybel import (readfile, Outputfile)

import time
import json
import pandas
import django
from decimal import *
from rdkit import Chem
from rdkit.Chem.Descriptors import ExactMolWt, MolWt
from rdkit.Chem.rdMolDescriptors import CalcMolFormula
from rdkit.Chem.inchi import MolToInchi
from rdkit.Chem.inchi import MolToInchiKey
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Draw
# from rdkit.Chem.Draw import IPythonConsole #Needed to show molecules
# Only needed if modifying defaults
from rdkit.Chem.Draw.MolDrawing import MolDrawing, DrawingOptions
import os

import requests

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MCDB.settings")
django.setup()
from app import models

# Create your tests here.

# getcontext().prec = 6

# mol = Chem.MolFromSmiles(
#     'O=C(C=C([N+]1(CCOCC1)COC(CCC(N[C@@H](CCCNC([NH3])=N)C(NCC(N[C@@H](CC([O])=O)C(N[C@@H](CO)C([O-])=O)=O)=O)=O)=O)=O)O2)C3=C2C(C4=CC=CC=C4)=CC=C3')
# print(Decimal(ExactMolWt(mol)).quantize(Decimal('0.00')))
# print(CalcMolFormula(mol))
# print(MolToInchi(mol))
# print(MolToInchiKey(mol))
# inchi=MolToInchi(mol)
# print(inchi[6:])

# mol1 = Chem.MolFromSmiles('O=C(N[C@@H](CC1CCCCC1)C(N[C@@H](C[C@@H]2CCNC2=O)C([H])=O)=O)C3=CC4=C(N3)C=CC=C4')
# mol2 = Chem.MolFromSmiles('S=C(N(C)C)N/N=C(C)/C1=NC=CC=C1')
# fp1 = FingerprintMols.FingerprintMol(mol1)
# fp2 = FingerprintMols.FingerprintMol(mol2)
# print(DataStructs.FingerprintSimilarity(fp1, fp2))

# res=os.system('blastp -query  a1.fa  -db  MCDB')
# print(res)

# database=models.gene.objects.all()
# print(database.get(gene='CDT1'))

# opts = DrawingOptions()
# m = Chem.MolFromSmiles('O=C1C(CO)(CO)N2CCC1CC2')
# # opts.includeAtomNumbers=True
# # opts.bondLineWidth=2.8
# draw = Draw.MolToImage(m, options=opts)
# draw.save('MCDB/static/test.jpg')

def MolFormatConversion(input_file: str, output_file: str, input_format="smi", output_format="mol2"):
    molecules = readfile(input_format, input_file)
    output_file_writer = Outputfile(output_format, output_file)
    for i, molecule in enumerate(molecules):
        output_file_writer.write(molecule)
    output_file_writer.close()
    print('%d molecules converted' % (i+1))



# /home/xiaoming/Cynthia -q /home/xiaoming/web/MCDB/MCDB/static/data/ccompare/1.mol2 -t /home/xiaoming/web/MCDB/MCDB/static/data/ccompare/2.mol2 -o output -n 300 -sCutoff 0.2

# database=models.compound.objects.all()
# file=open('MCDB/static/data/ccompare/all.smi','w')
# for data in database:
#     print(data.smiles,file=file)
# file.close()

MolFormatConversion('MCDB/static/data/ccompare/1.smi',
                    'MCDB/static/data/ccompare/1.mol2')