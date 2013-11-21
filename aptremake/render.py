
from collections import defaultdict
from data import Type

def render_horizontal_axes(design, display, data):
     # FIXME: Can have more than one hpos / vpos encoding.
    hpos = design.hpos() # X->Y
    if hpos:
        display["haxis"] = True
        hpos = hpos[0]
        haxes_domain = hpos.facts.dependent
        if design.marktype() == "bar":
            haxes_domain = hpos.facts.determinant
        if haxes_domain.type == Type.ordinal:
            display["hpos_ordinal"] = True
            display["hordering"] = dict(zip(haxes_domain.tuples, range(len(haxes_domain.tuples))))
        if haxes_domain.type == Type.nominal:
            display["hpos_nominal"] = True
        display["hlabel"] = haxes_domain.name
        if design.marktype() == "bar":
            for (mark, hpos) in hpos.facts.tuples:
                data[mark]["mark"] = mark
                data[mark]["hpos"] = mark
        else:
            for (mark, hpos) in hpos.facts.tuples:
                data[mark]["mark"] = mark
                data[mark]["hpos"] = hpos

def render_vertical_axes(design, display, data):
    # FIXME: Can have more than one hpos / vpos encoding.
    vpos = design.vpos() # X->Z
    if vpos:
        display["vaxis"] = True
        vpos = vpos[0]
        if vpos.facts.dependent.type == Type.ordinal:
            display["vpos_ordinal"] = True
            display["vordering"] = dict(zip(vpos.facts.dependent.tuples, range(len(vpos.facts.dependent.tuples))))
        if vpos.facts.dependent.type == Type.nominal:
            display["vpos_nominal"] = True
        display["vlabel"] = vpos.facts.name
        for (mark, vpos) in vpos.facts.tuples:
            data[mark]["mark"] = mark
            data[mark]["vpos"] = vpos

def render_color(design, display, data):
    color = design.color() # X or X->W
    if color:
        color = color[0]
        display["color"] = True
        display["colorlabel"] = color.facts.name
        if color.facts.arity == 2:    
            if color.facts.dependent.type == Type.ordinal:
                display["color_ordinal"] = True
                display["colorordering"] = dict(zip(color.facts.dependent.tuples, range(len(color.facts.dependent.tuples))))
            for (mark, color) in color.facts.tuples:
                data[mark]["mark"] = mark
                data[mark]["color"] = color
        elif color.facts.arity == 1:
            if color.facts.type == Type.ordinal:
                display["color_ordinal"] = True
                display["colorordering"] = dict(zip(range(len(color.facts.tuples)), color.facts.tuples))
            for mark in color.facts.tuples:
                data[mark]["mark"] = mark
                data[mark]["color"] = mark

def render(design):
    display = {}
    data = defaultdict(dict)

    display["marktype"] = design.marktype()
    
    render_horizontal_axes(design, display, data)
    render_vertical_axes(design, display, data)     
    render_color(design, display, data)    
    
    data = data.values()

    display["data"] = data
    print display
    return display

