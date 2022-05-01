
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
import os
import bs4
import requests
import hashlib

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

# genes = models.gene.objects.all()
# print(genes.get(gene='CDT1').level)
# compounds = models.compounds.objects.all()
# cnt=-1
# for compound in compounds:
#     cnt+=1
# #     if cnt<3897:
# #         continue
#     print(cnt)
#     print(compound.gene)
#     if compound.gene=='tubulin':
#         continue
#     compound.level=genes.filter(gene=compound.gene)[0].level
#     compound.save()

# genes = models.gene.objects.all()
# print(genes.get(gene='CDT1').level)
# pdbs = models.pdb.objects.all()
# cnt=-1
# for pdb in pdbs:
#     cnt+=1
#     # if cnt<3897:
#     #     continue
#     print(cnt)
#     print(pdb.gene)
#     gene=genes.filter(uniprotKB=pdb.gene)[0]
#     pdb.level=gene.level
#     pdb.uniprot=gene.uniprotKB
#     pdb.gene=gene.gene
#     pdb.save()


# compounds = models.compound.objects.all()
# res = {}
# level = {}
# cnt = 1
# for compound in compounds:
#     print(cnt)
#     cnt += 1
#     name = compound.gene
#     level[name] = compound.level
#     if name in res:
#         res[name] += 1
#     else:
#         res[name] = 1

# res = sorted(res.items(), key=lambda x: x[1], reverse=True)
# # print(res)

# models.figc.objects.all().delete()
# cnt = 0
# mx=res[0][1]
# for x in res:
#     cnt += 1
#     print(cnt)
#     models.figc.objects.create(
#         id=cnt,
#         gene=x[0],
#         number=x[1],
#         level=level[x[0]],
#         factor=x[1]/mx
#     )

# database=models.figc.objects.all()
# x=database[0]
# x.level=1
# x.save()

# level = {}
# genes=models.gene.objects.all()
# for gene in genes:
#     level[gene.gene]=gene.level

# pdbs = models.pdb.objects.all()
# res = {}
# cnt = 1
# for pdb in pdbs:
#     print(cnt)
#     cnt += 1
#     name = pdb.gene
#     if name in res:
#         res[name] += 1
#     else:
#         res[name] = 1

# res = sorted(res.items(), key=lambda x: x[1], reverse=True)
# print(res)

# models.figd.objects.all().delete()
# cnt = 0
# mx=res[0][1]
# for x in res:
#     cnt += 1
#     print(cnt)
#     models.figd.objects.create(
#         id=cnt,
#         gene=x[0],
#         number=x[1],
#         level=level[x[0]],
#         factor=x[1]/mx
#     )
def getMol2(target):
    md5=str(hashlib.md5(target.encode('utf8')).hexdigest())
    if os.path.exists('MCDB/static/data/ccompare/mol2/'+md5+'.mol2'):
        return
    cookies = {
        '_ga': 'GA1.2.1397624577.1614268347',
        '_gid': 'GA1.2.1052693397.1615095820',
        'session': '.eJw9zMEKgkAQANBfiTl3yFwvgoeNtWWD2QhWZOYilCW6WlBBtuK_56n3AW-Cqq0hnWB1hhSo63vb7VrrzIhDPmJgzxoFBZ-g2ndWn2Iu8y0FymBew-X1vFXvh7_e_wUrE7GT4uiKwKqJUNPXlocWtR2sKxIqjUAnl67ZoDIxOfywzJZu_gE7eSvy.EyYCmQ.jSw8-Ak-Io3seAenec9ziC_zL_o',
    }

    headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'DNT': '1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Referer': 'http://zinc.docking.org/substances/home/',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    }

    params = (
        ('q', target),
    )

    response = requests.get('http://zinc.docking.org/substances/search/', headers=headers, params=params, cookies=cookies, verify=False)
    #NB. Original query string below. It seems impossible to parse and
    #reproduce query strings 100% accurately so the one below is given
    #in case the reproduced version is not "correct".
    # response = requests.get('http://zinc.docking.org/substances/search/?q=O%3DC1C%28CO%29%28CO%29N2CCC1CC2', headers=headers, cookies=cookies, verify=False)

    soup = bs4.BeautifulSoup(response.text, "html5lib")
    text = soup.find(class_='zinc-id').a['href']
    print(text)

    zincID=text

    cookies = {
        '_ga': 'GA1.2.1397624577.1614268347',
        '_gid': 'GA1.2.1052693397.1615095820',
        'session': '.eJw9zMEKgkAQANBfiTl3yFwvgoeNtWWD2QhWZOYilCW6WlBBtuK_56n3AW-Cqq0hnWB1hhSo63vb7VrrzIhDPmJgzxoFBZ-g2ndWn2Iu8y0FymBew-X1vFXvh7_e_wUrE7GT4uiKwKqJUNPXlocWtR2sKxIqjUAnl67ZoDIxOfywzJZu_gE7eSvy.EyX_qQ.SOBVcWoNsn0S8UjAT0HkP11wBzQ',
    }

    headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'DNT': '1',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Referer': 'http://zinc.docking.org/substances/search/?q=O%3DC1C%28CO%29%28CO%29N2CCC1CC2',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
    }

    response = requests.get('http://zinc.docking.org'+zincID, headers=headers, cookies=cookies, verify=False)
    soup=bs4.BeautifulSoup(response.text,"html5lib")
    text=soup.find(title='Downloads').div.ul.find('a',string='Mol2')['href']
    print(text)
    file=requests.get(text)
    open('MCDB/static/data/ccompare/mol2/'+md5+'.mol2.gz','wb').write(file.content)
    os.system('gzip MCDB/static/data/ccompare/mol2/'+md5+'.mol2.gz -d')


database = models.compound.objects.all()
cnt = 0
for data in database:
    print(cnt)
    cnt += 1
    if cnt<=1750:
        continue
    try:
        print(data.smiles)
        getMol2(data.smiles)
        print('success')
    except KeyboardInterrupt:
        break
    except:
        print('failure')
        continue
