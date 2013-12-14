
from collections import OrderedDict
from data import load

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

    def __init__(self, marktype, markclass, marktag):
        self.marktype = marktype
        self.markclass = markclass
        self.marktag = marktag

Marks = {
    "POINTS": Mark(Mark.MarkType.point, Mark.MarkClass.dot, Mark.MarkTag.circle), 
    "BARS": Mark(Mark.MarkType.bar, Mark.MarkClass.bar, Mark.MarkTag.rect)
}

class Subplot(object):

    def __init__(self, marks):
        self.ridx = 0
        self.cidx = 0
        self.haxis = False
        self.vaxis = False
        self.marks = marks
        self.hpos = None
        self.hpos_nominal = False
        self.hpos_ordinal = False
        self.hordering = None
        self.hlabel = ""
        self.vpos = None
        self.vpos_nominal = False
        self.vpos_ordinal = False
        self.vordering = None
        self.vlabel = ""

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

    def __init__(self, subplots={}, data=[]):
        self.subplots = subplots
        self.nrows = 0
        self.ncols = 0
        if len(subplots) > 0:
            self.nrows = max([s.ridx+1 for s in subplots.itervalues()])
            self.ncols = max([s.cidx+1 for s in subplots.itervalues()])
        self.haxes = dict([(s.ridx, s.hpos) for s in subplots.itervalues()])
        self.vaxes = dict([(s.cidx, s.vpos) for s in subplots.itervalues()])
        self.data = data
        self.tasks = OrderedDict()
        self.color = None
        self.color_ordinal = False
        self.cordering = None

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

