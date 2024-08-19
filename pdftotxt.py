#!/usr/bin/env python3

import os
import sys
import time
from pathlib import Path
import requests

if (args_count := len(sys.argv)) > 3:
    print(f'At most two arguments expected, got {args_count - 1}')
    raise SystemExit(2)
elif args_count < 3:
    pdf_path = Path(__file__).parent.resolve()
    txt_path = Path(sys.arv[1])
else:
    pdf_path = Path(sys.argv[1])
    txt_path = Path(sys.argv[2])

print(f'Converting files from {pdf_path} to {txt_path}.')

start = time.time()
ext = ('.pdf')
l_files = []
for path, dirs, files in os.walk(pdf_path):
    l_files.extend(files)
    for name in files:
        if name.endswith(ext):
            pdf_filename = os.path.join(path, name)
            print(f'Processing {pdf_filename}')
            out = requests.post('http://localhost:8000/upload', files={'file': open(pdf_filename, 'rb')})
            if out.status_code != 200:
                print(f'Server Error: response {out.status_code}')
            out = out.json()
            #token = out['token']
            #methods = out['methods']
            #discussion = out['discussion']
            all = out['all']
            txt_filename = os.path.join(txt_path,os.path.splitext(name)[0]) + '.txt'
            #print(txt_filename)
            open(txt_filename, 'w', encoding='utf-8').write(all)

end = time.time()
print('Folder processed')
t_elapsed = round((end - start)/60, 3)
print(f'Stopped after {t_elapsed} minutes, processing at a rate of {t_elapsed/len(l_files)} minutes per file with a total of {len(l_files)} files.')
