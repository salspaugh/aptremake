

import matplotlib.pyplot as plt

def render(design):
    d = {}
    data = {}
    
    hpos = design.hpos() # X->Y
    if hpos: # FIXME: Can have more than one hpos / vpos encoding.
        d["haxis"] = True
        data["marks"] = [t[0] for t in hpos.facts.tuples]
        data["hpos"] = [t[1] for t in hpos.facts.tuples]
    
    vpos = design.vpos() # X->Z
    if vpos:
        d["vaxis"] = True
        if data["marks"]:
            data["vpos"] = [0]*len(data["marks"])
            for (k,v) in vpos.facts.tuples:
                idx = data["marks"].index(k)
                data["vpos"][idx] = v
        else:
            data["marks"] = [t[0] for t in vpos.facts.tuples]
            data["hpos"] = [t[1] for t in vpos.facts.tuples]
    
    color = design.color() # X or X->W
    if color:
        d["color"] = True
        if data["marks"]:
            data["color"] = [0]*len(data["marks"])
            for (k,v) in color.facts.tuples:
                idx = data["marks"].index(k)
                data["color"][idx] = v
        else:
            data["marks"] = [t[0] for t in color.facts.tuples]
            data["color"] = [t[1] for t in color.facts.tuples]

    d["data"] = data
    return d

