#! /bin/bash

# have python installed (3.9.0 is what I usw)
# have node installed

pip install -r data/requirements.txt
python data/run.py dbexport.csv data/data-json.mustache ./
npm run build
