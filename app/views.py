import os
from django.shortcuts import redirect, render
import json
import pandas
from rdkit import Chem
from rdkit.Chem import Draw
from rdkit import DataStructs
from rdkit.Chem.Fingerprints import FingerprintMols
from app import models
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.http import FileResponse, StreamingHttpResponse
import random
import string
import hashlib
import pickle
import csv
import requests
import bs4
import re
# Create your views here.


def test(request):
    return render(request, 'test.html')


def blank(request):
    return redirect('index_html/')


def index_html(request):
    return render(request, 'index.html')


def getMol2(target):
    md5 = str(hashlib.md5(target.encode('utf8')).hexdigest())
    if os.path.exists('MCDB/static/data/ccompare/temp/'+md5+'.mol2'):
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

    response = requests.get('http://zinc.docking.org/substances/search/',
                            headers=headers, params=params, cookies=cookies, verify=False)
    # NB. Original query string below. It seems impossible to parse and
    # reproduce query strings 100% accurately so the one below is given
    # in case the reproduced version is not "correct".
    # response = requests.get('http://zinc.docking.org/substances/search/?q=O%3DC1C%28CO%29%28CO%29N2CCC1CC2', headers=headers, cookies=cookies, verify=False)

    soup = bs4.BeautifulSoup(response.text, "html5lib")
    text = soup.find(class_='zinc-id').a['href']
    # print(text)

    zincID = text

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

    response = requests.get('http://zinc.docking.org'+zincID,
                            headers=headers, cookies=cookies, verify=False)
    soup = bs4.BeautifulSoup(response.text, "html5lib")
    text = soup.find(title='Downloads').div.ul.find('a', string='Mol2')['href']
    file = requests.get(text)
    filePath = 'MCDB/static/data/ccompare/temp/'+md5+'.mol2.gz'
    open(filePath, 'wb').write(file.content)
    os.system('gzip '+filePath+' -d')


@csrf_exempt
def data_html(request):
    params1 = 30
    params2 = 30
    if request.method == 'GET':
        params1 = int(request.GET['params1'])
        params2 = int(request.GET['params2'])
    elif request.method == 'POST':
        params1 = int(request.POST['params1'])
        params2 = int(request.POST['params2'])
    data_2_1 = []
    database = models.figc.objects.all()
    for x in database[:params1]:
        data_2_1.append(
            [x.gene, x.factor, x.number, x.level])
    data_2_1.reverse()
    random.shuffle(data_2_1)
    data_2_2 = []
    database = models.figd.objects.all()
    for x in database[:params2]:
        data_2_2.append(
            [x.gene, x.factor, x.number, x.level])
    data_2_2.reverse()
    random.shuffle(data_2_2)
    return render(request, 'data.html', {'data_2_1': json.dumps(data_2_1),
                                         'data_2_2': json.dumps(data_2_2),
                                         'params1': params1,
                                         'params2': params2})


def gene_html(request):
    return render(request, 'gene.html')


def compound_html(request):
    return render(request, 'compound.html')


def pdb_html(request):
    return render(request, 'pdb.html')


def ccompare_html(request):
    return render(request, 'ccompare.html')


def pcompare_html(request):
    return render(request, 'pcompare.html')


def upload_html(request):
    return render(request, 'upload.html')


@csrf_exempt
def gene_search(request):
    text = ''
    page = 1
    if request.method == 'POST':
        text = request.POST['text']
        page = request.POST['page']
    elif request.method == 'GET':
        text = request.GET['text']
        page = request.GET['page']
    text = text.strip()
    if text == '':
        return render(request, 'gene.html', {'msg': 'Please enter query parameters.'})
    if text[0:5] == 'level':
        database = models.gene.objects.filter(level=text[5])
    else:
        d1 = models.gene.objects.filter(gene__contains=text)
        d2 = models.gene.objects.filter(uniprotKB__contains=text)
        database = d1 | d2
    paginator = Paginator(database, 10)
    # print(paginator.num_pages)
    if len(database) == 0:
        return render(request, 'gene.html', {'msg': 'This gene has not been confirmed as MC-related gene. Please contact us for update if any proof articles have been published.'})
    else:
        return render(request, 'gene.html',
                      {'check': True,
                       'text': text,
                       'datas': paginator.page(page),
                       'totalPages': paginator.num_pages,
                       'currentPage': page})


@csrf_exempt
def go_search(request):
    text = ''
    page = 1
    if request.method == 'POST':
        text = request.POST['text']
        page = request.POST['page']
    elif request.method == 'GET':
        text = request.GET['text']
        page = request.GET['page']

    data = models.gene.objects.filter(gene=text)[0]
    goid = data.go.split('|')
    term = data.goterm.split('|')
    res = []
    for i in range(len(goid)):
        res.append({'goid': goid[i], 'term': term[i]})
    paginator = Paginator(res, 10)
    # print(paginator.num_pages)
    return render(request, 'go.html',
                  {'check': True,
                   'text': text,
                   'datas': paginator.page(page),
                   'totalPages': paginator.num_pages,
                   'currentPage': page})


@csrf_exempt
def compound_search(request):
    text = ''
    page = 1
    numberPerPage = 10
    if request.method == 'POST':
        text = request.POST['text']
        page = request.POST['page']
        if 'numberPerPage' in request.POST:
            numberPerPage = request.POST['numberPerPage']
    elif request.method == 'GET':
        text = request.GET['text']
        page = request.GET['page']
        if 'numberPerPage' in request.GET:
            numberPerPage = request.GET['numberPerPage']
    if text == '':
        return render(request, 'compound.html', {'msg': 'Please enter query parameters.'})
    try:
        numberPerPage = int(numberPerPage)
    except:
        numberPerPage = 10
    text = text.strip()
    d1 = models.compound.objects.filter(gene__contains=text)
    d2 = models.compound.objects.filter(uniprotKB__contains=text)
    d3 = models.compound.objects.filter(smiles__contains=text)
    d4 = models.compound.objects.filter(InChI__contains=text)
    d5 = models.compound.objects.filter(InChIKey__contains=text)
    d6 = models.compound.objects.filter(prop__contains=text)
    database = d1 | d2 | d3 | d4 | d5 | d6
    if 'sort' in request.GET:
        database = database.order_by(request.GET['sort'])
    paginator = Paginator(database, numberPerPage)
    datas = paginator.page(page)
    for data in datas:
        md5 = str(hashlib.md5(data.smiles.encode('utf8')).hexdigest())
        data.md5 = md5
        filename = 'MCDB/static/img/tmp/'+md5+'.jpg'
        if not os.path.exists(filename):
            m = Chem.MolFromSmiles(data.smiles)
            draw = Draw.MolToImage(m)
            draw.save(filename)
    # print(paginator.num_pages)
    if len(database) == 0:
        return render(request, 'compound.html', {'msg': 'This compound has not been confirmed as MC-related compound. Please contact us for update if any proof articles have been published.'})
    else:
        return render(request, 'compound.html',
                      {'check': True,
                       'text': text,
                       'datas': datas,
                       'totalPages': paginator.num_pages,
                       'currentPage': page,
                       'numberPerPage': numberPerPage})


@csrf_exempt
def pdb_search(request):
    text = ''
    page = 1
    if request.method == 'POST':
        text = request.POST['text']
        page = request.POST['page']
    elif request.method == 'GET':
        text = request.GET['text']
        page = request.GET['page']
    d1 = models.pdb.objects.filter(uniprot__contains=text)
    d2 = models.pdb.objects.filter(gene__contains=text)
    database = d1 | d2
    if text == '':
        return render(request, 'pdb.html', {'msg': 'Please enter query parameters.'})
    text = text.strip()
    if 'sort' in request.GET:
        sort=request.GET['sort']
        if sort=='date':
            database = database.order_by('-'+request.GET['sort'])
        else:
            database = database.order_by(request.GET['sort'])
    paginator = Paginator(database, 10)
    # print(paginator.num_pages)
    if len(database) == 0:
        return render(request, 'pdb.html', {'msg': 'This gene has not been confirmed as MC-related gene. Please contact us for update if any proof articles have been published.'})
    else:
        return render(request, 'pdb.html',
                      {'check': True,
                       'text': text,
                       'datas': paginator.page(page),
                       'totalPages': paginator.num_pages,
                       'currentPage': page})


@csrf_exempt
def ccompare_search(request):
    text = ''
    page = 1
    algorithm = 'SHAFTS'
    if request.method == 'POST':
        text = request.POST['text']
        page = request.POST['page']
        if 'algorithm' in request.POST:
            algorithm = request.POST['algorithm']
    elif request.method == 'GET':
        text = request.GET['text']
        page = request.GET['page']
        if 'algorithm' in request.GET:
            algorithm = request.GET['algorithm']
    if text == '':
        return render(request, 'ccompare.html', {'msg': 'Please enter query parameters.'})
    text = text.strip()
    prefix = 'MCDB/static/data/ccompare/temp/'
    if algorithm == 'SHAFTS':
        randname = str(hashlib.md5(text.encode('utf8')).hexdigest())
        filename = prefix+randname
        datas = []
        try:
            getMol2(text)
            if not os.path.exists(prefix+randname+'Result.list'):
                os.system('/home/xiaoming/Cynthia -q MCDB/static/data/ccompare/temp/'+randname +
                        '.mol2 -t  MCDB/static/data/ccompare/all.mol2 -o MCDB/static/data/ccompare/temp/'+randname+' -n 300 -sCutoff 1')
            file = open(prefix+randname+'Result.list', 'r')
            for line in file.readlines():
                line = line.split('\t')
                if line[0] == 'Rank':
                    continue
                smiles = line[1]
                data = models.compound.objects.filter(smiles=smiles)[0]
                datas.append({
                    'smiles': data.smiles,
                    'HybridScore': line[2],
                    'ShapeScore': line[3],
                    'FeatureScore': line[4],
                    'prop': data.prop,
                    'gene': data.gene,
                    'uniprot': data.uniprotKB,
                    'level': data.level
                })
        except:
            return render(request, 'ccompare.html', {'msg': 'An error occurred.'})

        if 'sort' in request.GET:
            sort = request.GET['sort']
            if sort=='gene' or sort=='prop' or sort=='level' or sort=='uniprot':
                datas.sort(key=lambda x:x[sort])
            else:
                datas.sort(key=lambda x: float(x[sort]),reverse=True)
    else:
        randname = str(hashlib.md5(
            (text+'tanimoto').encode('utf8')).hexdigest())
        filename = prefix+randname
        if not os.path.exists(filename):
            datas = []
            try:
                mol1 = Chem.MolFromSmiles(text)
                fp1 = FingerprintMols.FingerprintMol(mol1)
                database = models.compound.objects.filter()
                for data in database:
                    mol2 = Chem.MolFromSmiles(data.smiles)
                    fp2 = FingerprintMols.FingerprintMol(mol2)
                    res = DataStructs.FingerprintSimilarity(fp1, fp2)
                    datas.append({
                        'smiles': data.smiles,
                        'similarity': round(res, 4),
                        'prop': data.prop,
                        'gene': data.gene,
                        'uniprot': data.uniprotKB,
                        'level': data.level
                    })
            except:
                return render(request, 'ccompare.html', {'msg': 'Illegal input.'})
            datas.sort(key=lambda x: x['similarity'], reverse=True)
            file = open(filename, 'wb')
            pickle.dump(datas, file)
            file.close()
            file = open(filename+'.csv', 'w', newline='')
            output = csv.writer(file)
            output.writerow(['Uniprot_Accession', 'Gene_Name', 'Classification',
                             'Confidence_Level', 'Similarity_Score', 'SMILES'])
            for data in datas:
                output.writerow(([data['uniprot'], data['gene'], data['prop'],
                                  data['level'], data['similarity'], data['smiles']]))
            # print(datas[0])
        else:
            file = open(filename, 'rb')
            datas = pickle.load(file)
            file.close()
        if 'sort' in request.GET:
            sort = request.GET['sort']
            if sort=='gene' or sort=='prop' or sort=='level' or sort=='uniprot':
                datas.sort(key=lambda x:x[sort])
            else:
                datas.sort(key=lambda x: float(x[sort]),reverse=True)
                
    paginator = Paginator(datas, 10)
    return render(request, 'ccompare.html',
                  {'check': True,
                   'text': text,
                   'name': randname,
                   'datas': paginator.page(page),
                   'totalPages': paginator.num_pages,
                   'currentPage': page,
                   'algorithm': algorithm})


@csrf_exempt
def pcompare_search(request):
    # randname = ''.join(random.choices(
    #     string.ascii_letters + string.digits, k=8))
    text = ''
    page = 1
    if request.method == 'POST':
        text = request.POST['text']
        page = request.POST['page']
    elif request.method == 'GET':
        text = request.GET['text']
        page = request.GET['page']
    if text == '':
        return render(request, 'pcompare.html', {'msg': 'Please enter query parameters.'})
    text = text.strip()
    prefix = 'MCDB/static/data/pcompare/'
    randname = str(hashlib.md5(text.encode('utf8')).hexdigest())
    if not os.path.exists(prefix+randname+'.txt'):
        with open(prefix+randname+'.fa', 'w') as f:
            f.write(text)
        res = os.system(
            'blastp -query '+prefix+randname+'.fa -db MCDB/static/data/MCDB/MCDB -out '+prefix+randname+'.txt')
    datas = []
    with open(prefix+randname+'.txt', 'r') as f:
        for line in f.readlines():
            if line[0] == '>':
                name = line[4:10]
                gene = models.gene.objects.filter(uniprotKB=name)[0].gene
                level = models.gene.objects.filter(uniprotKB=name)[0].level
            elif line[0:6] == 'Length':
                length = line[7:]
            elif line[1:6] == 'Score':
                fk = line.split(',')
                score = fk[0].split('=')[1]
                expect = fk[1].split('=')[1]
            elif line[1:11] == 'Identities':
                fk = line.split(',')
                identities = fk[0].split('=')[1]
                positives = fk[1].split('=')[1]
                gaps = fk[2].split('=')[1]
                datas.append({'name': name,
                              'length': length,
                              'gene': gene,
                              'level': level,
                              'score': score,
                              'expect': expect,
                              'identities': identities, 'positives': positives,
                              'gaps': gaps})

    if 'sort' in request.GET:
        sort = request.GET['sort']
        if sort == 'expect':
            datas.sort(key=lambda x: float(x[sort]))
        elif sort == 'length':
            datas.sort(key=lambda x: x[sort], reverse=True)
        elif sort == 'level':
            datas.sort(key=lambda x: x[sort])
        elif sort == 'gaps':
            datas.sort(key=lambda x: float(re.findall(
                r'[(](.*?)[)]', x[sort])[0].replace('%', '')))
        else:
            datas.sort(key=lambda x: float(re.findall(
                r'[(](.*?)[)]', x[sort])[0].replace('%', '')), reverse=True)

    paginator = Paginator(datas, 10)
    # print(os.getcwd())
    # print(text)
    # print(paginator.num_pages)
    # print(text.replace('\n', '%0A').replace('\r','%0A').strip())
    return render(request, 'pcompare.html',
                  {'check': True,
                   'text': text.replace('\n', '%0A').replace('\r', '%0A').replace('>', '%3E'),
                   'textshow': text,
                   'name': randname,
                   'datas': paginator.page(page),
                   'totalPages': paginator.num_pages,
                   'currentPage': page})


def pcdownload(request):
    name = request.GET['name']
    file = open('MCDB/static/data/pcompare/'+name+'.txt', 'rb')
    response = FileResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="result.txt"'
    return response


def ccdownload(request):
    name = request.GET['name']
    file = open('MCDB/static/data/ccompare/'+name+'.csv', 'rb')
    response = FileResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="result.csv"'
    return response


def cdownload(request):
    file = open('MCDB/static/data/compound.csv', 'rb')
    response = FileResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="MC-related compound.csv"'
    return response


def gdownload(request):
    file = open('MCDB/static/data/gene.csv', 'rb')
    response = FileResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="MC-related gene and protein.csv"'
    return response


def gene_upload(request):
    return render(request, 'upload.html', {'gmsg': 'Thank you for your submit.<br>we will review and update gene data as soon as possible'})


def compound_upload(request):
    return render(request, 'upload.html', {'cmsg': 'Thank you for your submit.<br>we will review and update compound data as soon as possible'})
