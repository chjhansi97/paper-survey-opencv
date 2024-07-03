import os
import random
import json
import shutil
from PIL import Image
folders = [f for f in os.listdir('w2_data/extracted')]
pages = [i for i in range(3, 15)]
print(folders)
selected = {}

profile = {
    "0": {
        "total": 0
    },
    "1": {
        "total": 0
    },
    "2": {
        "total": 0
    },
    "3": {
        "total": 84,
        "q": {
            "1": [
                2,
                9
            ],
            "2": [
                9,
                16
            ],
            "3": [
                16,
                23
            ],
            "4": [
                23,
                30
            ],
            "5": [
                30,
                37
            ],
            "6": [
                37,
                44
            ],
            "7": [
                44,
                51
            ],
            "8": [
                51,
                58
            ],
            "9": [
                58,
                65
            ],
            "10": [
                65,
                72
            ],
            "11": [
                72,
                79
            ],
            "12": [
                79,
                86
            ]
        }
    },
    "4": {
        "total": 60,
        "q": {
            "13": [
                2,
                7
            ],
            "14": [
                7,
                12
            ],
            "15": [
                12,
                17
            ],
            "16": [
                17,
                22
            ],
            "17": [
                22,
                27
            ],
            "18": [
                27,
                32
            ],
            "19": [
                32,
                37
            ],
            "20": [
                37,
                42
            ],
            "21": [
                42,
                47
            ],
            "22": [
                47,
                52
            ],
            "23": [
                52,
                57
            ],
            "24": [
                57,
                62
            ]
        }
    },
    "5": {
        "total": 43,
        "q": {
            "25": [
                2,
                7
            ],
            "26": [
                7,
                12
            ],
            "27": [
                12,
                17
            ],
            "28": [
                17,
                22
            ],
            "29": [
                22,
                27
            ],
            "30": [
                27,
                33
            ],
            "31": [
                33,
                39
            ],
            "32": [
                39,
                45
            ]
        }
    },
    "6": {
        "total": 65,
        "q": {
            "33": [
                2,
                7
            ],
            "34": [
                7,
                12
            ],
            "35": [
                12,
                17
            ],
            "36": [
                17,
                22
            ],
            "37": [
                22,
                27
            ],
            "38": [
                27,
                32
            ],
            "39": [
                32,
                37
            ],
            "40": [
                37,
                42
            ],
            "41": [
                42,
                47
            ],
            "42": [
                47,
                52
            ],
            "43": [
                52,
                57
            ],
            "44": [
                57,
                62
            ],
            "45": [
                62,
                67
            ]
        }
    },
    "7": {
        "total": 55,
        "q": {
            "46": [
                2,
                7
            ],
            "47": [
                7,
                12
            ],
            "48": [
                12,
                17
            ],
            "49": [
                17,
                22
            ],
            "50": [
                22,
                29
            ],
            "51": [
                29,
                36
            ],
            "52": [
                36,
                43
            ],
            "53": [
                43,
                50
            ],
            "54": [
                50,
                57
            ]
        }
    },
    "8": {
        "total": 70,
        "q": {
            "55": [
                2,
                9
            ],
            "56": [
                9,
                16
            ],
            "57": [
                16,
                23
            ],
            "58": [
                23,
                30
            ],
            "59": [
                30,
                37
            ],
            "60": [
                37,
                44
            ],
            "61": [
                44,
                51
            ],
            "62": [
                51,
                58
            ],
            "63": [
                58,
                65
            ],
            "64": [
                65,
                72
            ]
        }
    },
    "9": {
        "total": 43,
        "q": {
            "65": [
                2,
                9
            ],
            "66": [
                9,
                16
            ],
            "67": [
                16,
                23
            ],
            "68": [
                23,
                30
            ],
            "69": [
                30,
                35
            ],
            "70": [
                35,
                40
            ],
            "71": [
                40,
                45
            ]
        }
    },
    "10": {
        "total": 65,
        "q": {
            "72": [
                2,
                7
            ],
            "73": [
                7,
                12
            ],
            "74": [
                12,
                17
            ],
            "75": [
                17,
                22
            ],
            "76": [
                22,
                27
            ],
            "77": [
                27,
                32
            ],
            "78": [
                32,
                37
            ],
            "79": [
                37,
                42
            ],
            "80": [
                42,
                47
            ],
            "81": [
                47,
                52
            ],
            "82": [
                52,
                57
            ],
            "83": [
                57,
                62
            ],
            "84": [
                62,
                67
            ]
        }
    },
    "11": {
        "total": 60,
        "q": {
            "85": [
                2,
                7
            ],
            "86": [
                7,
                12
            ],
            "87": [
                12,
                17
            ],
            "88": [
                17,
                22
            ],
            "89": [
                22,
                27
            ],
            "90": [
                27,
                32
            ],
            "91": [
                32,
                37
            ],
            "92": [
                37,
                42
            ],
            "93": [
                42,
                47
            ],
            "94": [
                47,
                52
            ],
            "95": [
                52,
                57
            ],
            "96": [
                57,
                62
            ]
        }
    },
    "12": {
        "total": 43,
        "q": {
            "97": [
                2,
                7
            ],
            "98": [
                7,
                12
            ],
            "99": [
                12,
                17
            ],
            "100": [
                17,
                24
            ],
            "101": [
                24,
                31
            ],
            "102": [
                31,
                38
            ],
            "103": [
                38,
                45
            ]
        }
    },
    "13": {
        "total": 57,
        "q": {
            "104": [
                2,
                9
            ],
            "105": [
                9,
                16
            ],
            "106": [
                16,
                23
            ],
            "107": [
                23,
                30
            ],
            "108": [
                30,
                37
            ],
            "109": [
                37,
                44
            ],
            "110": [
                44,
                49
            ],
            "111": [
                49,
                54
            ],
            "112": [
                54,
                59
            ]
        }
    },
    "14": {
        "total": 21,
        "q": {
            "113": [
                2,
                7
            ],
            "114": [
                7,
                12
            ],
            "115": [
                12,
                17
            ]
        }
    },
    "15": {
        "total": 0
    }
}

for i in range(250):
    selected[random.choice(folders)] = random.choice(pages)

for k, v in selected.items():
    if k == "494c-001" or k == "405032":
        continue
    shutil.copyfile(f'w2_data/extracted/{k}/{v}.jpg', f'w2_data/QA/{k}.jpg')
    with open(f'w2_data/QA/{k}.html', 'w') as html:
        html.write(
            """<html><body><head><style>
                .parent {
                  border: 1px solid black;
                  margin: 1rem;
                  padding: 2rem 2rem;
                  text-align: center;
                }
                 .child {
                  display: inline-block;
                  border: 1px solid black;
                  padding: 1rem 1rem;
                  vertical-align: middle;
                }
                table tr td {
                border: 1px solid black;
                }
                </style> 
                <div class="parent">
                
            """
        )
        html.write(
            f"""
                            <h1>{k}</h1>              
                            <table class="child">
                            <tr>
                            <th>Image</th>
                            </tr>
                            <tr><td><img src='{k}.jpg' width='600px' height='auto'></td></tr>
                            </table>
                            """
        )

        survey_file = open(f'w2_data/corrected_jsondata/{k}.json', 'r')
        survey_data = json.loads(survey_file.read())
        html.write("""
            <table class="child">
            <tr><th>question</th><th>answer</th></tr>
        """)
        for x in profile[str(v)]['q'].keys():
            html.write(
                f"""  
                <tr><td>{x}</td><td>{survey_data[x]}</td></td></tr>"""
            )

        html.write(f"""</table></div></body></html>""")

print(selected)