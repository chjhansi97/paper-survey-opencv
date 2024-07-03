import os
import json
with open('w2_data/w2_manual_entries.csv') as csv:
    next(csv)
    for line in csv:
        l = line.split(';')
        objid = l[0]
        d = {
            "116":l[1],
            "117": l[2],
            "118": l[3],
            "119": l[4],
            "120a": l[5],
            "120b": l[6],
            "120c": l[7],
            "121a": l[8],
            "121b": l[9],
            "121c": l[10],
            "121d": l[11],
            "121e": l[12],
            "121f": l[13],
        }
        for k,v in d.items():
            if not v:
                d[k] = 'NULL'
            if not k == '120c' and not k == '121f' and not d[k] == 'NULL':
                d[k] = int(v)

        try:
            with open(os.path.join('w2_data','corrected_jsondata',f'{objid}.json')) as jfile:
                data = json.loads(jfile.read())
                data.update(d)
                #print(data)
        except FileNotFoundError:
            print("missing", objid)
            raise

        with open(os.path.join('w2_data','corr_append_data',f'{objid}.json'),'w') as outfile:
            outfile.write(json.dumps(data,indent=4))


