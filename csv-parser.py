import csv
import json
import chevron

with open('dbexport.csv', newline='', encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile, fieldnames=['artist', 'title', 'id', 'filepath'])
    fieldsToKeep = ['artist', 'title']
    data = [dict((k, v) for k, v in row.items() if k in fieldsToKeep) for row in reader]

with open('search-js.mustache', 'r', encoding="utf-8") as f:
    with open('search.js', 'w', encoding = "utf-8") as jsfile:
        newdata = map(lambda row: json.dumps(row), data)
        preparedjson = ','.join(newdata)
        result = chevron.render(f, { "songs": preparedjson })
        #undo the encoding that chevron does:
        jsfile.write(result.replace('&quot;', '"'))
        #also need to do the same with ampersands

