#!/usr/bin/env python3

import json
import os
import sys
import requests
import time
from pathlib import Path
from tqdm import tqdm  # Import tqdm for progress bar

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

with tqdm(total=len(l_files), desc="Processing Files", unit="file") as pbar:
    for path, dirs, files in os.walk(path_of_the_directory):
        l_files.extend(files)
        for name in files:
            if name.endswith(ext):
                pdf_filename = os.path.join(path, name)
                print(f'Processing {pdf_filename}')
                db_check = requests.post('http://localhost:8000/dbcheck', json = {'filename': name})
                if db_check.status_code != 200:
                    print(f'Server Error: response {db_check.status_code}')
                db_check = db_check.json()
                db_check = db_check['filename_exists']
                if db_check:
                    print('Paper already screened')
                    continue
                out = requests.post('http://localhost:8000/upload', files={'file': open(pdf_filename, 'rb')})
                if out.status_code != 200:
                    print(f'Server Error: response {out.status_code}')
                out = out.json()
                token = out['token']
                methods = out['methods']
                discussion = out['discussion']
                all = out['all']
                screening = requests.post('http://localhost:8000/dbupdate', json={'token': out['token'], 'methods': out['methods'], 'discussion': out['discussion'], 'all': out['all'], 'filename': name, 'generate_report': True})
               
                if screening.status_code != 200:
                    print(f'Server Error: response {screening.status_code}')
                report = screening.json()
                report = report['html']
                report_path = f'temp/reports/{os.path.splitext(name)[0]}.html'
                print(f'Saving report as {report_path}')
                with open(report_path, 'w') as f:
                    f.write(report)
                    f.close()
                print('Success')

                pbar.update(1)
                
end = time.time()
print('Folder processed')
t_elapsed = round((end - start)/60, 3)
print(f'Stopped after {t_elapsed} minutes, processing at a rate of {t_elapsed/len(l_files)} minutes per file with a total of {len(l_files)} files.')

