#!/usr/bin/env python3

import json
import os
import sys
import requests
import time
from pathlib import Path


if (args_count := len(sys.argv)) > 2:
    print(f"One argument expected, got {args_count - 1}")
    raise SystemExit(2)
elif args_count < 2:
    path_of_the_directory = Path(__file__).parent.resolve()
else:
    path_of_the_directory = Path(sys.argv[1])


print(path_of_the_directory)
start = time.time()
ext = ('.pdf')
l_files = []
for path, dirs, files in os.walk(path_of_the_directory):
    l_files.extend(files)
    for name in files:
        if name.endswith(ext):
            pdf_filename = os.path.join(path, name)
            print(f'Processing {pdf_filename}')
            #db_check = requests.post('http://localhost:8000/dbcheck', json = {'filename': name}) 
            #if db_check.status_code != 200:
            #    print(f'Server Error: response {db_check.status_code}')
            #db_check = db_check.json()
            #db_check = db_check['filename_exists'] 
            #if db_check:
            #    print('Paper already screened')
            #    continue
            out = requests.post('http://localhost:8000/upload', files={'file': open(pdf_filename, 'rb')})
            if out.status_code != 200:
                print(f'Server Error: response {out.status_code}')
            out = out.json()
            token = out['token']
            methods = out['methods']
            discussion = out['discussion']
            all = out['all']
            screening = requests.post('http://localhost:8000/dbupdate', json={'token': out['token'], 'methods': out['methods'], 'discussion': out['discussion'], 'all': out['all'], 'filename': name})
            if screening.status_code != 200:
                print(f'Server Error: response {screening.status_code}')
            else:
                print('Success')
end = time.time()
print('Folder processed')
t_elapsed = round((end - start)/60, 3)
print(f'Stopped after {t_elapsed} minutes, processing at a rate of {t_elapsed/len(l_files)} minutes per file with a total of len(l_files) files.')

