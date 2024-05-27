import os
import json

errata_lookup = {}

with open('details.csv') as errata:
    next(errata)
    for line in errata:
        sid, question, answer = line.split(',')
        
        errata_lookup[sid] = {}

with open('details.csv') as errata:
    next(errata)
    for line in errata:
        sid, question, answer = line.split(',')
        
        errata_lookup[sid][question] = answer.replace("\n","")

with open('details.json', 'w') as out_file:
    out_file.write(json.dumps(errata_lookup, indent=4))

with open('details.json') as efile:
    e = json.loads(efile.read())

    for k, v in e.items():
        for key, value in v.items():
            if value != 'NULL':
                e[k][key] = int(value)
with open('details.json','w') as outfile:
    outfile.write(json.dumps(e, indent=4))

with open('details.json') as file:
    a = json.loads(file.read())

    for k,v in a.items():
        
        json_path = 'output_json/'+k+'.json'
        with open(json_path) as json_file:
            data = json.load(json_file)
            
            for key,value in v.items():
                #print(data[key])
                data[key] = value
                

        with open(json_path, 'w') as ofile:
            
            json.dump(data, ofile, indent=4)