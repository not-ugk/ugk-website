import csv
import json
import chevron
import argparse
import generate_recent_songs
from argparse import Namespace

def parse_args(args):
    parser = argparse.ArgumentParser('Process OpenKj\'s dbexport.csv.')
    parser.add_argument('dbexport')
    parser.add_argument('template')
    parser.add_argument('targetdir')

    return parser.parse_args(args)

def read_db_export(filename):
    with open(filename, newline='', encoding="iso-8859-1") as csvfile:
        reader = csv.DictReader(csvfile, fieldnames=['artist', 'title', 'id', 'filepath'])
        fieldsToKeep = ['artist', 'title', 'id']
        return [dict((k, v) for k, v in row.items() if k in fieldsToKeep) for row in reader]

def write_json(data, template, target):
    with open(template, 'r', encoding="utf-8") as f:
        with open(target, 'w', encoding = "iso-8859-1") as jsfile:
            newdata = map(toJson, data)
            preparedjson = ','.join(newdata)
            result = chevron.render(f, { "songs": preparedjson })
            jsfile.write(fix_encoding(result))

def write_csv(data, target):
    with open(target, "w", encoding = "iso-8859-1") as csvfile:
        csv.DictWriter(csvfile, fieldnames=['artist', 'title', 'id', 'date_added']).writerows(data)

def toJson(data: dict[str, str]):
    data["id"] = fix_id(data["id"])
    return json.dumps(data)

def fix_id(id: str):
    return id.replace(' ', '_')

def fix_encoding(text: str):
    #undo the encoding that chevron does, plus some other fixes.
    return text.replace('&quot;', '"').replace('&amp;', '&').replace("AC?DC", "AC/DC")

def sort_recently_added(song):
    return song["date_added"]

def run(parsed_args: Namespace):
    data = read_db_export(parsed_args.dbexport)

    #TODO: Why is this empty
    recently_added = generate_recent_songs.fetch_recently_added()

    print(len(list(recently_added.keys())))
    for song in recently_added:
        print("song!")

        print(str(song))

    updated_data = []
    for entry in data:
        updated_entry = entry
        print(f'ID: {entry["id"]}')
        if entry["id"] in recently_added:
            updated_entry["date_added"] = str(recently_added[entry["id"]].first_encountered.date)
        else:
            print(f'missing id in recently added: {entry["id"]}')
            updated_entry["date_added"] = "2020-01-01"
        updated_data.append(updated_entry)

    #write full song list
    write_json(updated_data, parsed_args.template, parsed_args.targetdir + "data.json")

    #write recently_added.csv as side effect
    updated_data.sort(key = sort_recently_added)
    write_csv(updated_data, parsed_args.targetdir + "recently_added.csv")
