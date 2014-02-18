
from collections import OrderedDict
from metadata import load
from copy import deepcopy

class Mark(object): # This is a weird way to handle this.
# Done this way because we need to somehow record all the various CSS classes 
# and tags to use.

    class MarkType(object):

        point = "point"
        bar = "bar"

    class MarkClass(object):
        
        dot = "dot"
        bar = "bar"

    class MarkTag(object):
        
        circle = "circle"
        rect = "rect"

    def __init__(self, marktype, markclass, marktag, metadata, coding=None):
        self.marktype = marktype
        self.markclass = markclass
        self.marktag = marktag
        self.metadata = metadata
        self.coding = coding 

    def is_scatterplot_mark(self):
        return self.marktype == Mark.MarkType.point

    def is_barchart_mark(self):
        return self.marktype == Mark.MarkType.bar

def bind_marks(marktype, markclass, marktag):
    def mark(binding, coding=None):
        return Mark(marktype, markclass, marktag, binding, coding)
    return mark

Marks = {
    "POINTS": bind_marks(Mark.MarkType.point, Mark.MarkClass.dot, Mark.MarkTag.circle), 
    "BARS": bind_marks(Mark.MarkType.bar, Mark.MarkClass.bar, Mark.MarkTag.rect)
}

class Subplot(object):

    def __init__(self):
        self.ridx = 0
        self.cidx = 0
        self.haxis = False
        self.marks = None
        self.hpos = None
        self.hpos_coding = None
        self.hpos_nominal = False
        self.hpos_ordinal = False
        self.hpos_quantitative = False
        self.hordering = None
        self.hlabel = ""
        self.vaxis = False
        self.vpos = None
        self.vpos_coding = None
        self.vpos_nominal = False
        self.vpos_ordinal = False
        self.vpos_quantitative = False
        self.vordering = None
        self.vlabel = ""

    def __repr__(self):
        s = "HAXIS: " + str(self.hpos) + "; VAXIS: " + str(self.vpos)
        return s
    
    # TODO: Remove unnecessary deepcopy operations.
    def copy_haxis(self, design):
        self.haxis = deepcopy(design.haxis)
        self.hpos = deepcopy(design.hpos)
        self.hpos_coding = deepcopy(design.hpos_coding)
        self.hpos_nominal = deepcopy(design.hpos_nominal)
        self.hpos_ordinal = deepcopy(design.hpos_ordinal)
        self.hpos_quantitative = deepcopy(design.hpos_quantitative)
        self.hordering = deepcopy(design.hordering)
        self.hlabel = deepcopy(design.hlabel)
    
    def copy_vaxis(self, design):
        self.vaxis = deepcopy(design.vaxis)
        self.vpos = deepcopy(design.vpos)
        self.vpos_coding = deepcopy(design.vpos_coding)
        self.vpos_nominal = deepcopy(design.vpos_nominal)
        self.vpos_ordinal = deepcopy(design.vpos_ordinal)
        self.vpos_quantitative = deepcopy(design.vpos_quantitative) 
        self.vordering = deepcopy(design.vordering)
        self.vlabel = deepcopy(design.vlabel)

    def render(self, label_points=True):
        return {
            "ridx": self.ridx,
            "cidx": self.cidx,
            "hasHaxis": bool(self.haxis),
            "hasVaxis": bool(self.vaxis),
            "markType": self.marks.marktype,
            "markClass": self.marks.markclass,
            "markTag": self.marks.marktag,
            "markLabel": self.marks.metadata if label_points else None,
            "markCoding": self.marks.coding,
            "haxis": {
                "pos": self.hpos,
                "coding": self.hpos_coding,
                "nominal": self.hpos_nominal,
                "ordinal": self.hpos_ordinal,
                "quantitative": self.hpos_quantitative,
                "ordering": self.hordering,
                "label": self.hlabel,
            },
            "vaxis": {
                "pos": self.vpos,
                "coding": self.vpos_coding,
                "nominal": self.vpos_nominal,
                "ordinal": self.vpos_ordinal,
                "quantitative": self.vpos_quantitative,
                "ordering": self.vordering,
                "label": self.vlabel
            }
        }

class Design(object):

    def __init__(self, subplots=None):
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
        self.tasks = OrderedDict()
        self.color = None
        self.color_coding = None
        self.color_nominal = False
        self.color_ordinal = False
        self.cordering = None

    def copy_color(self, design):
        self.color = deepcopy(design.color)
        self.color_coding = deepcopy(design.color_coding)
        self.color_nominal = deepcopy(design.color_nominal)
        self.color_ordinal = deepcopy(design.color_ordinal)
        self.cordering = deepcopy(design.cordering)

    def render(self, view, label_points=True):
        return {
            "nrows": self.nrows,
            "ncols": self.ncols,
            "hasColor": bool(self.color),
            "color": self.color,
            "colorCoding": self.color_coding,
            "colorNominal": self.color_nominal,
            "colorOrdinal": self.color_ordinal,
            "cordering": self.cordering,
            "subplots": [s.render(label_points=label_points) for s in self.subplots.itervalues()],
            "caption": view.caption,
            "data": load(view)
        }

    def __repr__(self): # TODO: Fix these to be consistent with Python convention.
        s = "COLOR: " + str(self.color)
        s += "\nHAXES: " + str(self.haxes)
        s += "\nVAXES: " + str(self.vaxes)
        s += "\nSUBPLOTS: " 
        for (idx, subplot) in self.subplots.iteritems():
            s += "\n\t" + str(idx) + ": " + str(subplot)
        return s
