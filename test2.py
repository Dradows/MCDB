# import re
# import os
# import django
import hashlib

# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MCDB.settings")
# django.setup()

# from app import models

# datas=models.compound.objects.filter(gene='tubulin')
# for data in datas:
#     data.level=1
#     data.save()

# database = models.compound.objects.all()
# file = open('MCDB/static/data/ccompare/all.mol2', 'w')
# cnt = 0
# for data in database:
#     smiles = data.smiles
#     print(cnt)
#     cnt += 1
#     md5 = str(hashlib.md5(smiles.encode('utf8')).hexdigest())
#     tempPath = 'MCDB/static/data/ccompare/mol2/'+md5+'.mol2'
#     if os.path.exists(tempPath):
#         temp = open(tempPath,'r')
#         for line in temp:
#             if 'ZINC' in line and len(line)==17:
#                 file.write(smiles+'\n')
#             else:
#                 file.write(line)
#         file.write('\n\n')

# print(int("132"))
smiles='O=C(N[C@@H](CC1CCCCC1)C(N[C@@H](C[C@@H]2CCNC2=O)C([H])=O)=O)C3=CC4=C(N3)C=CC=C4'
md5 = str(hashlib.md5(smiles.encode('utf8')).hexdigest())

print(md5)