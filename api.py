from fastapi import FastAPI, UploadFile, File, Request
from fastapi.responses import FileResponse
from secrets import token_hex
from utils.extractor import pdftools
import os
import time
from jetfighter import jetfighter
from limitation_recognizer import limitation_recognizer
from trial_identifier import trial_identifier
from barzooka import barzooka
from sciscore import sciscore
from oddpub import oddpub
from rtransparent import rtransparent
import shutil
from unidecode import unidecode
from generate_html import generate_html
import subprocess
import psycopg2
import json
import uvicorn

app = FastAPI()


@app.post('/upload')
async def upload(file: UploadFile = File(...)):
    token = token_hex(16)
    if os.path.exists('temp'):
        shutil.rmtree('temp')
    os.mkdir('temp', 0o777)
    os.mkdir('temp/discussion')
    os.mkdir('temp/methods')
    os.mkdir('temp/all_text')
    os.mkdir('temp/oddpub_text', 0o777)
    os.mkdir('temp/images')
    f_name = f'temp/{token}.pdf'
    contents = await file.read()
    open(f_name, 'wb').write(contents)
    pdf = pdftools.PDF(f_name, token)
    pdf.get_images(False)
    return {'token': token, 'methods': unidecode(pdf.get_text('methods')), 'discussion': unidecode(pdf.get_text('discussion')), 'all': unidecode(pdf.get_text('all'))}

@app.post('/report')
async def report(request: Request):
    r = await request.json()
    discussion = r['discussion']
    methods = r['methods']
    token = r['token']
    all = r['all']
    filename = r['filename']
    open(f'temp/discussion/{token}.txt', 'w', encoding='utf-8').write(discussion)
    open(f'temp/methods/{token}.txt', 'w', encoding='utf-8').write(methods)
    open(f'temp/all_text/{token}.txt', 'w', encoding='utf-8').write(all)
    print(filename)
    print('running oddpub')
    oddpub_results = oddpub()
    print('running jetfighter')
    jetfighter_results = jetfighter(False, 1)
    print('running limitation')
    limitation_recognizer_results = limitation_recognizer()
    print('running trial id')
    trial_identifier_results = trial_identifier([token])
    print('running sciscore')
    sciscore_results = sciscore()
    print('running barzooka')
    barzooka_results = barzooka()
    print('running rtransparent')
    rtransparent_results = rtransparent()
    html = generate_html(token, filename, jetfighter_results, limitation_recognizer_results, trial_identifier_results, sciscore_results, barzooka_results, oddpub_results, rtransparent_results)
    open(f'pdfs/{token}.html', 'w').write(html.replace('<div style="width:600px; margin:0 auto;">', '<div style="width:600px;">').replace('width: 300px;', 'width: 200px;'))
    subprocess.call(f'weasyprint pdfs/{token}.html pdfs/{token}.pdf -p', shell=True)
    return {'html': html}


@app.post('/dbupdate')
async def dbupdate(request: Request):
    r = await request.json()
    token = r['token']
    filename = r['filename']
    discussion = r['discussion']
    methods = r['methods']
    all = r['all']
    generate_report = r['generate_report']
    open(f'temp/discussion/{token}.txt', 'w', encoding='utf-8').write(discussion)
    open(f'temp/methods/{token}.txt', 'w', encoding='utf-8').write(methods)
    open(f'temp/all_text/{token}.txt', 'w', encoding='utf-8').write(all)
    print(filename)
    # connection with the database inside the container
    try:
        conn = psycopg2.connect(dbname='papers', port=5432, user='postgres', host='pipeline-database', password=os.environ['POSTGRES_PASSWORD'])
        cur = conn.cursor()
        # create table papers if it does not exist
        cur.execute(
                    '''create table if not exists papers (
                        id integer primary key generated always as identity,
                        filename text unique,
                        discussion_text text,
                        methods_text text,
                        all_text text,
                        jet_page_numbers json,
                        limitation_sentences json,
                        trial_numbers json,
                        sciscore json,
                        is_modeling_paper boolean,
                        graph_types json,
                        is_open_data boolean,
                        is_open_code boolean,
                        reference_check json,
                        coi_statement boolean,
                        funding_statement boolean,
                        registration_statement boolean
                        )'''
                        )
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

    print('running oddpub')
    oddpub_results = oddpub()
    print('running jetfighter')
    jetfighter_results = jetfighter(False, 1)
    print('running limitation')
    limitation_recognizer_results = limitation_recognizer()
    print(limitation_recognizer_results)
    print('running trial id')
    trial_identifier_results = trial_identifier([token])
    print(trial_identifier_results)
    print('running sciscore')
    sciscore_results = sciscore()
    print(sciscore_results)
    print('running barzooka')
    barzooka_results = barzooka()
    print(barzooka_results)
    print('running rtransparent')
    rtransparent_results = rtransparent()
    print(rtransparent_results)

    print('updating database')
    cur.execute('''
    insert into papers (filename, discussion_text, methods_text, all_text,
    jet_page_numbers, limitation_sentences, trial_numbers, sciscore, is_modeling_paper,
    graph_types, is_open_data, is_open_code, 
    coi_statement, funding_statement, registration_statement
    )
    values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) on conflict (filename) do update
    ''',
    (filename, discussion, methods, all,
    json.dumps(jetfighter_results[token]['page_nums']),
    json.dumps(limitation_recognizer_results[token]['sents']),
    json.dumps(trial_identifier_results[token]['trial_identifiers']),
    json.dumps(sciscore_results[token]['raw_json']),
    sciscore_results[token]['is_modeling_paper'],
    json.dumps(barzooka_results[token]['graph_types']),
    oddpub_results[token]['open_data'],
    oddpub_results[token]['open_code'],
    rtransparent_results[token]['coi_statement'],
    rtransparent_results[token]['funding_statement'],
    rtransparent_results[token]['registration_statement']
    ))
    conn.commit()
    print('database update completed')

    if generate_report==True:
        html = generate_html(token, filename, jetfighter_results, limitation_recognizer_results, trial_identifier_results, sciscore_results, barzooka_results, oddpub_results, rtransparent_results)
        print(f'generated report for {filename}')
        return {'html': html}


@app.post('/dbcheck')
async def dbcheck(request: Request):
    filename_exists = False
    r = await request.json()
    filename = r['filename']
    # connection with the database inside the container
    try:
        conn = psycopg2.connect(dbname='papers', port=5432, user='postgres', host='pipeline-database', password=os.environ['POSTGRES_PASSWORD'])
        cur = conn.cursor()
        cur.execute('select filename from papers where filename = %s', (filename,))
        if cur.fetchone():
            filename_exists = True
    except (Exception, psycopg2.DatabaseError) as error:
        print(f'{error}, could not connect to database')
    cur.close()
    return {'filename_exists': filename_exists}


@app.get('/pdf')
async def pdf(token):
    return FileResponse(f'pdfs/{token}.pdf')

@app.post('/rawlimitations')
async def rawlimitations(request: Request):
    r = await request.json()
    discussion = r['discussion']
    token = r['token']
    filename = r['filename']
    open(f'temp/discussion/{token}.txt', 'w', encoding='utf-8').write(discussion)
    print(filename)
    print('running limitation')
    limitation_recognizer_results = limitation_recognizer()
    print(limitation_recognizer_results)
    #html = generate_html(token, filename, jetfighter_results, limitation_recognizer_results, trial_identifier_results, sciscore_results, barzooka_results, oddpub_results, rtransparent_results)
    #open(f'pdfs/{token}.html', 'w').write(html.replace('<div style="width:600px; margin:0 auto;">', '<div style="width:600px;">').replace('width: 300px;', 'width: 200px;'))
    #subprocess.call(f'weasyprint pdfs/{token}.html pdfs/{token}.pdf -p', shell=True)
    return {filename: json.dumps(limitation_recognizer_results[token]['sents'])}

#if __name__ == "__main__":
#    uvicorn.run("api:app", host="127.0.0.1", reload=True, port=8002)
