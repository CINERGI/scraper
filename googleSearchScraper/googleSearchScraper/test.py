import json
from pprint import pprint

data = []
with open('spider4_metadata_abstractmissingonly_pdf_title.json') as data_file:
    #for line in data_file:
        #data.append(json.load(line))
    data = json.load(data_file)
pprint(data['title'])
