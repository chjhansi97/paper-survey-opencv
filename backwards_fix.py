import os
import json
count = 1
from shutil import copyfile, rmtree

mapping = {
    0: 15,
    1: 14,
    2: 13,
    3: 12,
    4: 11,
    5: 10,
    6: 9,
    7: 8,
    8: 7,
    9: 6,
    10: 5,
    11: 4,
    12: 3,
    13: 2,
    14: 1,
    15: 0,
}

for base, dirs, files in os.walk('w2_data/flip'):
    if os.path.isdir(os.path.join(base, 'fix')):
        rmtree(os.path.join(base, 'fix'))


    for f in files:
        if not os.path.isdir(os.path.join(base, 'fix')):
            os.makedirs(os.path.join(base, 'fix'))
        if f.endswith('.jpg') and '_' in f:
            #os.remove(os.path.join(base,f))
            copyfile(os.path.join(base,f), os.path.join(base,f.replace('_','')))
            # #copyfile(os.path.join(base, f), os.path.join('data','jsondata',f))
            #x = f.split(".")
            #print(x[0])
            #print(mapping[int(x[0])])
            #print("#"*20)
            #print(base)
            #copyfile(os.path.join(base, f), os.path.join(base, f"_{mapping[int(x[0])]}.jpg"))

            #with open(os.path.join(base,f)) as j:
                #print(len(json.loads(j.read())))
