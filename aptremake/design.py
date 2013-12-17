
from collections import OrderedDict
from data import load
from copy import deepcopy

class Mark(object):

    class MarkType(object):

        point = "point"
        bar = "bar"

    class MarkClass(object):
        
        dot = ".dot"
        bar = ".bar"

    class MarkTag(object):
        
        circle = "circle"
        rect = "rect"

    def __init__(self, marktype, markclass, marktag, data):
        self.marktype = marktype
        self.markclass = markclass
        self.marktag = marktag
        self.data = data

def bind_marks(marktype, markclass, marktag):
    def mark(binding):
        return Mark(marktype, markclass, marktag, binding)
    return mark

Marks = {
    "POINTS": bind_marks(Mark.MarkType.point, Mark.MarkClass.dot, Mark.MarkTag.circle), 
    "BARS": bind_marks(Mark.MarkType.bar, Mark.MarkClass.bar, Mark.MarkTag.rect)
}

class Subplot(object):

    def __init__(self, marks):
        self.ridx = 0
        self.cidx = 0
        self.haxis = False
        self.marks = marks
        self.hpos = None
        self.hpos_nominal = False
        self.hpos_ordinal = False
        self.hordering = None
        self.hlabel = ""
        self.vaxis = False
        self.vpos = None
        self.vpos_nominal = False
        self.vpos_ordinal = False
        self.vordering = None
        self.vlabel = ""

    def __repr__(self):
        s = "HAXIS: " + str(self.hpos) + "; VAXIS: " + str(self.vpos)
        return s

    def copy_haxis(self, design):
        self.haxis = deepcopy(design.haxis)
        self.hpos = deepcopy(design.hpos)
        self.hpos_nominal = deepcopy(design.hpos_nominal)
        self.hpos_ordinal = deepcopy(design.hpos_ordinal)
        self.hordering = deepcopy(design.hordering)
        self.hlabel = deepcopy(design.hlabel)
    
    def copy_vaxis(self, design):
        self.vaxis = deepcopy(design.vaxis)
        self.vpos = deepcopy(design.vpos)
        self.vpos_nominal = deepcopy(design.vpos_nominal)
        self.vpos_ordinal = deepcopy(design.vpos_ordinal)
        self.vordering = deepcopy(design.vordering)
        self.vlabel = deepcopy(design.vlabel)

    def render(self):
        return {
            "ridx": self.ridx,
            "cidx": self.cidx,
            "hasHaxis": bool(self.haxis),
            "hasVaxis": bool(self.vaxis),
            "markType": self.marks.marktype,
            "markClass": self.marks.markclass,
            "markTag": self.marks.marktag,
            "hpos": self.hpos,
            "hpos_nominal": self.hpos_nominal,
            "hpos_ordinal": self.hpos_ordinal,
            "hordering": self.hordering,
            "hlabel": self.hlabel,
            "vpos": self.vpos,
            "vpos_nominal": self.vpos_nominal,
            "vpos_ordinal": self.vpos_ordinal,
            "vordering": self.vordering,
            "vlabel": self.vlabel
        }

class Design(object):

    def __init__(self, subplots=None, data=None):
        self.subplots = subplots if subplots else {}
        self.nrows = 0
        self.ncols = 0
        if subplots and len(self.subplots) > 0:
            self.nrows = max([s.ridx+1 for s in self.subplots.itervalues()])
            self.ncols = max([s.cidx+1 for s in self.subplots.itervalues()])
        self.haxes = {}
        self.vaxes = {}
        if subplots:
            self.haxes = dict([(s.ridx, s.hpos) for s in self.subplots.itervalues()])
            self.vaxes = dict([(s.cidx, s.vpos) for s in self.subplots.itervalues()])
        self.data = data
        self.tasks = OrderedDict()
        self.color = None
        self.color_ordinal = False
        self.cordering = None

    def copy_color(self, design):
        self.color = deepcopy(design.color)
        self.color_ordinal = deepcopy(design.color_ordinal)
        self.cordering = deepcopy(design.cordering)

    def render(self):
        return {
            "nrows": self.nrows,
            "ncols": self.ncols,
            "hasColor": bool(self.color),
            "color": self.color,
            "color_ordinal": self.color_ordinal,
            "cordering": self.cordering,
            "subplots": [s.render() for s in self.subplots.itervalues()],
            "data": load(self.data)
        }

    def __repr__(self): # TODO: Fix these to be consistent with Python convention.
        s = "COLOR: " + str(self.color)
        s += "\nHAXES: " + str(self.haxes)
        s += "\nVAXES: " + str(self.vaxes)
        s += "\nSUBPLOTS: " 
        for (idx, subplot) in self.subplots.iteritems():
            s += "\n\t" + str(idx) + ": " + str(subplot)
        return s
