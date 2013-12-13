
from collections import OrderedDict
from data import load

class Mark(object):

    class MarkType(object):

        point = "POINT"
        bar = "BAR"

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
        self.vpos = None
    
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
            "vpos": self.vpos
        }

class Design(object):

    def __init__(self, subplots={}, data=[]):
        self.subplots = subplots
        self.nrows = max([s.ridx+1 for s in subplots.itervalues()])
        self.ncols = max([s.cidx+1 for s in subplots.itervalues()])
        self.haxes = dict([(s.ridx, s.haxis) for s in subplots.itervalues()])
        self.vaxes = dict([(s.cidx, s.vaxis) for s in subplots.itervalues()])
        self.data = data
        self.tasks = OrderedDict()
        self.color = None

    def render(self):
        return {
            "nrows": self.nrows,
            "ncols": self.ncols,
            "hasColor": bool(self.color),
            "color": self.color,
            "subplots": [s.render() for s in self.subplots.itervalues()],
            "data": load(self.data)
        }

