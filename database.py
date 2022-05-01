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
import re

import requests
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MCDB.settings")
django.setup()

from app.models import gene
from app.models import compound
from app.models import pdb


# ak = gene.objects.filter(gene='CCNA2').update(level=1)
# print(ak)

# def go(name):
#     cookies = {
#         'X-Mapping-ejmejipg': 'CCB807F0DB1FB1AB527DAC3C66846EC0',
#         '_ga': 'GA1.3.576173887.1595039565',
#         '_gid': 'GA1.3.1785065088.1595039565',
#         '_gat': '1',
#     }

#     headers = {
#         'Connection': 'keep-alive',
#         'accept': 'text/gpad',
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36',
#         'DNT': '1',
#         'Sec-Fetch-Site': 'same-origin',
#         'Sec-Fetch-Mode': 'cors',
#         'Sec-Fetch-Dest': 'empty',
#         'Referer': 'https://www.ebi.ac.uk/QuickGO/annotations?geneProductId=Q9UJX5',
#         'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
#     }

#     text = name

#     params = (
#         ('downloadLimit', '1000'),
#         ('geneProductId', text),
#     )

#     response = requests.get('https://www.ebi.ac.uk/QuickGO/services/annotation/downloadSearch',
#                             headers=headers, params=params, cookies=cookies)
#     # print(response.text.split('\n'))

#     goid=''

#     for line in response.text.split('\n'):
#         # print(line)
#         if len(line) == 0:
#             continue
#         if line[0]=='!':
#             continue
#         goid+=line.split()[3]+','
#         # for x in line.split():
#         #     print(x)
#     if len(goid)>0:
#         goid=goid[:-1]
#     headers = {
#         'Accept': 'application/json, text/plain, */*',
#         'Referer': 'https://www.ebi.ac.uk/QuickGO/annotations?geneProductId=Q9UJX5',
#         'DNT': '1',
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
#     }

#     response = requests.get(
#         'https://www.ebi.ac.uk/QuickGO/services/ontology/go/terms/'+goid, headers=headers)
#     js = json.loads(response.text)
#     goid = ''
#     term = ''
#     for x in js['results']:
#         goid += x['id']+'|'
#         term += x['name']+'|'
#     if len(goid) > 0:
#         goid = goid[:-1]
#     if len(term) > 0:
#         term = term[:-1]
#     return goid,term


getcontext().prec = 10

print('hello')

# es = []
# data = pandas.read_excel(io='data.xlsx', sheet_name=1)
# for index, row in data.iterrows():
#     # if (index==23):
#     #     print(str(row['fk1']))
#     print(index)
#     # if (index==1130):
#     #     break
#     goid=''
#     term=''
#     goid0=''
#     term0=''
#     if row['GO']!=row['GO']:
#         # print('empty')
#         goid,term=go(row['UniProtKB ID'])
#     else:
#         goid=row['GO']
#         term=row['GO Term']
#     if len(goid)>0:
#         goid0=goid.split('|')[0]
#     if len(term)>0:
#         term0=term.split('|')[0]
#     synonyms=row['Synonyms']
#     for i in range(1,10):
#         if (row['fk'+str(i)]!=row['fk'+str(i)]):
#             break
#         else:
#             if str(row['fk'+str(i)])=='2020-09-02 00:00:00':
#                 synonyms+=',2-Sep'
#             else:
#                 synonyms+=','+row['fk'+str(i)]
#     es.append(gene(id=index+1,
#                    go=goid,
#                    goterm=term,
#                    go0=goid0,
#                    goterm0=term0,
#                    protein=row['Protein Name'],
#                    gene=row['Gene'],
#                    synonyms=synonyms,
#                    uniprotKB=row['UniProtKB ID'],
#                    level=row['Confidence level']
#                    ))
# gene.objects.all().delete()
# gene.objects.bulk_create(es)


# data = pandas.read_excel(io='data.xlsx', sheet_name=1)
# for index, row in data.iterrows():
#     res=''
#     if row['PMID']==row['PMID']:
#         for x in str(row['PMID']).split(','):
#             x=x.strip()
#             res+='<u><a href="https://pubmed.ncbi.nlm.nih.gov/'+x+'/" target="_blank">'+x+'</a></u>,'
#         res=res[:-1]
#         gene.objects.filter(gene=row['Gene']).update(pmid=res)
#     else:
#         gene.objects.filter(gene=row['Gene']).update(pmid=res)


# for x in gene.objects.all():
#     if x.synonyms=='nan':
#         x.synonyms=''
#         x.save()

# datas = gene.objects.all()
# with open('MCDB/static/data/gene.csv','w') as file:
#     file.write('UniProt_Accession,Gene_Name,GO_Identifier,GO_Term,Protein_Name,Synonyms,Confidence_Level,MC_PMID\n')
#     for data in datas:
#         temp=''
#         if data.pmid is not None:
#             temp='|'.join(re.findall(r'/">(.+?)</a>',data.pmid))
#         file.write(data.uniprotKB+','+data.gene+','+data.go+','+data.goterm.replace(',',' ')+','+data.protein.replace(',','|')+','+data.synonyms.replace(',','|')+','+str(data.level)+','+temp+'\n')

datas = compound.objects.all()
with open('MCDB/static/data/compound.csv','w') as file:
    file.write('UniProt_Accession,Gene_Name,Confidence_Level,SMILES,InChI_Key,Molecular_Formula,Molecular_Weight,Classification\n')
    for data in datas:
        file.write(data.uniprotKB+','+data.gene+','+str(data.level)+','+data.smiles+','+data.InChIKey+','+data.MolecularFormula+','+data.MolecularWeight+','+data.prop+'\n')


# es = []
# name = pandas.read_excel(io='data.xlsx', sheet_name=1).iloc[:, [4, 15]]
# data = pandas.read_excel(io='data.xlsx', sheet_name=2)
# for index, row in data.iterrows():
#     # if row['smiles'] == 'PEP-1-SIRT2' or row['smiles'] == 'SRT-2379' or row['smiles'] == 'O=C(NCCCCCCCCCCC)CCCSCC.[K][Q]([*][R]C([3H])=S([G]([*])[K])[G])[3H]':
#     #     continue
#     # if index==5007:
#     #     mol = Chem.MolFromSmiles(row['SMILES'])
#     #     uniprot=''
#     #     if (row['Gene']!='tubulin'):
#     #         uniprot = name[name['Gene'] == row['Gene']].iloc[0, 1]
#     #     es.append(compound(id=index+1,
#     #                        uniprotKB=uniprot,
#     #                        gene=row['Gene'],
#     #                        InChI=MolToInchi(mol)[6:],
#     #                        InChIKey=MolToInchiKey(mol),
#     #                        MolecularFormula=CalcMolFormula(mol),
#     #                        MolecularWeight=Decimal(ExactMolWt(mol)).quantize(Decimal('0.00')),
#     #                        smiles=row['SMILES'],
#     #                        prop=row['property']
#     #                        ))
#     try:
#         mol = Chem.MolFromSmiles(row['SMILES'])
#         uniprot=''
#         if (row['Gene']!='tubulin'):
#             uniprot = name[name['Gene'] == row['Gene']].iloc[0, 1]
#         es.append(compound(id=index+1,
#                            uniprotKB=uniprot,
#                            gene=row['Gene'],
#                            InChI=MolToInchi(mol)[6:],
#                            InChIKey=MolToInchiKey(mol),
#                            MolecularFormula=CalcMolFormula(mol),
#                            MolecularWeight=Decimal(MolWt(mol)).quantize(Decimal('0.00')),
#                            smiles=row['SMILES'],
#                            prop=row['property']
#                            ))
#     except:
#         print(index, row['SMILES'])
#         continue
# compound.objects.all().delete()
# compound.objects.bulk_create(es)

# name = pandas.read_excel(io='data.xlsx').iloc[:, [4, 15]]
# # print(name[name['UniProtKB ID']=='Q9H211'])
# data = pandas.read_csv('../data/rcsb.csv')
# es = []
# for index, row in data.iterrows():
#     # res = ''
#     # # 去除nan
#     # if row['only in uniport'] == row['only in uniport']:
#     #     res = row['only in uniport']
#     # if row['only in pdb'] == row['only in pdb']:
#     #     if res == '':
#     #         res = row['only in pdb']
#     #     else:
#     #         res = res+','+row['only in pdb']
#     # if row['both'] == row['both']:
#     #     if res == '':
#     #         res = row['both']
#     #     else:
#     #         res = res+','+row['both']
# #     gene = name[name['UniProtKB ID'] == row['UniProtKB ID']].iloc[0, 0]
#     es.append(pdb(id=index+1,
#                   gene=row['UniProtKB ID'],
#                   pdb=row['pdb'],
#                   date=row['date'],
#                   method=row['method']
#                   ))
#     if index % 10 == 0:
#         print(index)
# pdb.objects.all().delete()
# pdb.objects.bulk_create(es)
