
from data import Type
from random import randint

def render(design):

    plot = {
        "numRows": 4,
        "numCols": 1,
        "hasColor": True,
        "color": "color",
        "subplots": [
            {
                "rowidx": 0,
                "colidx": 0,
                "hasHaxis": True,
                "hasVaxis": True,
                "markType": "point",
                "markClass": ".dot",
                "markTag": "circle",
                "hpos": "val",
                "vpos": "val" 
            },
            {
                "rowidx": 1,
                "colidx": 0,
                "hasHaxis": True,
                "hasVaxis": True,
                "markType": "point",
                "markClass": ".dot",
                "markTag": "circle",
                "hpos": "val",
                "vpos": "val" 
            },
            {
                "rowidx": 2,
                "colidx": 0,
                "hasHaxis": True,
                "hasVaxis": True,
                "markType": "point",
                "markClass": ".dot",
                "markTag": "circle",
                "hpos": "val",
                "vpos": "val" 
            },
            {
                "rowidx": 3,
                "colidx": 0,
                "hasHaxis": True,
                "hasVaxis": True,
                "markType": "point",
                "markClass": ".dot",
                "markTag": "circle",
                "hpos": "val",
                "vpos": "val" 
            },
            #{
            #    "rowidx": 1,
            #    "colidx": 1,
            #    "hasHaxis": True,
            #    "hasVaxis": True,
            #    "markType": "point",
            #    "markClass": ".dot",
            #    "markTag": "circle",
            #    "hpos": "val",
            #    "vpos": "val" 
            #},
            #{
            #    "rowidx": 1,
            #    "colidx": 2,
            #    "hasHaxis": True,
            #    "hasVaxis": True,
            #    "hasVaxis": True,
            #    "markType": "point",
            #    "markClass": ".dot",
            #    "markTag": "circle",
            #    "hpos": "val",
            #    "vpos": "val" 
            #}
        ],
        "data" : [
            {
                "id": 0,
                "val": randint(1,100),
                "color": 0
            },
            {
                "id": 1,
                "val": randint(1,100),
                "color": 1
            },
            {
                "id": 2,
                "val": randint(1,100),
                "color": 0
            },
            {
                "id": 3,
                "val": randint(1,100),
                "color": 1
            },
            {
                "id": 4,
                "val": randint(1,100),
                "color": 1
            },
            {
                "id": 5,
                "val": randint(1,100),
                "color": 0
            },
            {
                "id": 6,
                "val": randint(1,100),
                "color": 1
            },
            {
                "id": 7,
                "val": randint(1,100),
                "color": 0
            },
            {
                "id": 8,
                "val": randint(1,100),
                "color": 1
            },
            {
                "id": 9,
                "val": randint(1,100),
                "color": 0
            }
        ]
    }
    
    return plot

