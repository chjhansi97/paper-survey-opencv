import os
import json
import shutil

with open('output_json/100014.json') as efile:
    errata = json.loads(efile.read())


for file in os.listdir('data3/jsondata'):
    objid = file.split('.')[0]

    with open(os.path.join('data3','jsondata',file)) as f:
        if objid in errata:

            s = json.loads(f.read())
            s.pop('116')
            s.pop('117')
            s.update(errata[objid])
            #print(s)
            with open(os.path.join('data3', 'corrected_jsondata', file), 'w') as outfile:
                outfile.write(json.dumps(s))
        else:
            shutil.copyfile(os.path.join('data3','jsondata',file), os.path.join('data3', 'corrected_jsondata', file))