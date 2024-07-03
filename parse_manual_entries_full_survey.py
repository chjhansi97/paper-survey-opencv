import json
l = {
    "120": "120a",
    "121": "120b",
    "122": "120c",
    "123": "121a",
    "124": "121b",
    "125": "121c",
    "126": "121d",
    "127": "121e",
    "128": "121f",
}

with open('w2_data/w2_manual_entries_2_missing.csv') as f:
    next(f)
    for row in f:
        vals = row.replace('\n','').split(';')
        data = {}
        id = None
        for val in enumerate(vals):

            if val[0] == 0:
                id = val[1]
                continue
            if str(val[0]) in l:
                data[l[str(val[0])]] = val[1]
            else:
                data[str(val[0])] = val[1]

        with open(f"{id}.json", "w") as o:
            o.write(json.dumps(data))






