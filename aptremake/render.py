
from collections import defaultdict
from data import Type

def render(design):
    d = {}
    data = defaultdict(dict)
    
    hpos = design.hpos() # X->Y
    if hpos: # FIXME: Can have more than one hpos / vpos encoding.
        if hpos.facts.range.type == Type.ordinal:
            d["hpos_ordinal"] = True
        if hpos.facts.range.type == Type.nominal:
            d["hpos_nominal"] = True
        d["haxis"] = True
        d["hlabel"] = hpos.facts.name
        for (mark, hpos) in hpos.facts.tuples:
            data[mark]["mark"] = mark
            data[mark]["hpos"] = hpos
    
    vpos = design.vpos() # X->Z
    if vpos:
        if vpos.facts.range.type == Type.ordinal:
            d["vpos_ordinal"] = True
        if vpos.facts.range.type == Type.nominal:
            d["vpos_nominal"] = True
        d["vaxis"] = True
        d["vlabel"] = vpos.facts.name
        for (mark, vpos) in vpos.facts.tuples:
            data[mark]["mark"] = mark
            data[mark]["vpos"] = vpos
    
    color = design.color() # X or X->W
    if color:
        d["color"] = True
        d["colorlabel"] = color.facts.name
        if color.facts.arity == 2:    
            if color.facts.range.type == Type.ordinal:
                d["color_ordinal"] = True
            for (mark, color) in color.facts.tuples:
                data[mark]["mark"] = mark
                data[mark]["color"] = color
        elif color.facts.arity == 1:
            if color.facts.type == Type.ordinal:
                d["color_ordinal"] = True
            for mark in color.facts.tuples:
                data[mark]["mark"] = mark
                data[mark]["color"] = mark
    
    data = data.values()

    d["data"] = data
    return d

