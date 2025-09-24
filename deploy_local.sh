#! /bin/bash

# have python installed (3.9.0 is what I use)
# have node installed

pip install -r data/requirements.txt
python data/run.py dbexport.csv data/data-json.mustache data.json
#python data/run_recent_songs_parser.py data/data-json.mustache recentsongs.json
npm run build
