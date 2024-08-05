import csv
import json
import chevron

#todo: add unit tests or switch the whole script to js (and then add tests)
#todo: test for fixing chevron encodings 

with open('dbexport.csv', newline='', encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile, fieldnames=['artist', 'title', 'id', 'filepath'])
    fieldsToKeep = ['artist', 'title']
    data = [dict((k, v) for k, v in row.items() if k in fieldsToKeep) for row in reader]

with open('data-json.mustache', 'r', encoding="utf-8") as f:
    with open('data.json', 'w', encoding = "utf-8") as jsfile:
        newdata = map(lambda row: json.dumps(row), data)
        preparedjson = ','.join(newdata)
        result = chevron.render(f, { "songs": preparedjson })
        #undo the encoding that chevron does:
        jsfile.write(result.replace('&quot;', '"'))
        #also need to do the same with ampersands

