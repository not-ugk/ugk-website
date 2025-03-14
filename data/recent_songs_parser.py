import csv
import json
import chevron
import argparse
import generate_recent_songs
from argparse import Namespace

def parse_args(args):
    parser = argparse.ArgumentParser('Generate recent songs from git and create json.')
    parser.add_argument('template')
    parser.add_argument('target')

    return parser.parse_args(args)

file_name = "recentsongs.csv"
def generate_csv():
    lines = generate_recent_songs.write_song_updates()
    with open(file_name, "w", newline='') as file:
        for line in lines:
            file.write(line + '\n')

def run(parsed_args: Namespace):
    generate_csv()
    with open(file_name, newline='') as csvfile:
        reader = csv.DictReader(csvfile, fieldnames=['date', 'artist', 'title', 'id', 'filepath'])
        fieldsToKeep = ['date', 'artist', 'title', 'id']
        data = [dict((k, v) for k, v in row.items() if k in fieldsToKeep) for row in reader]

    with open(parsed_args.template, 'r', encoding="utf-8") as f:
        with open(parsed_args.target, 'w', encoding = "utf-8") as jsfile:
            newdata = map(toJson, data)
            preparedjson = ','.join(newdata)
            result = chevron.render(f, { "songs": preparedjson })
            jsfile.write(fix_encoding(result))

def toJson(data: dict[str, str]):
    data["id"] = fix_id(data["id"])
    return json.dumps(data)

def fix_id(id: str):
    return id.replace(' ', '_')

def fix_encoding(text: str):
    #undo the encoding that chevron does, plus some other fixes.
    return text.replace('&quot;', '"').replace('&amp;', '&').replace("AC?DC", "AC/DC").replace("\\u00eb", "ë").replace("\\u00e1", 'á')
