
from collections import defaultdict


class Objects(object):
    
    marks = "MARKS"
    haxis = "HAXIS"
    vaxis = "VAXIS"
    hpos = "HPOS"
    vpos = "VPOS"
    color = "COLOR"


class Encodes(object):
    
    def __init__(self, objects, facts, language):
        self.objects = objects
        self.facts = facts
        self.language = language

    def encodes_marks(self):
        return self.objects == Objects.marks

    def encodes_haxis(self):
        return self.objects == Objects.haxis

    def encodes_vaxis(self):
        return self.objects == Objects.vaxis

    def encodes_color(self):
        return self.objects == Objects.color

    def __repr__(self):
        return "Encodes(%s, %s, %s)" % (self.objects, self.facts, self.language)

def double_axes_composition(design):
    haxes = filter(lambda x: x.encodes_haxis(), design.encodings)
    vaxes = filter(lambda x: x.encodes_vaxis(), design.encodings)
    if len(haxes) == 2 and len(vaxes) == 2 and \
        haxes[0].facts.range == haxes[1].facts.range and \
        vaxes[0].facts.range == vaxes[1].facts.range:
        design.encodings.remove(haxes[1])
        design.encodings.remove(vaxes[1])
        # TODO: Adjust marks to differentiate them 

def single_axis_composition(design):
    haxes = filter(lambda x: x.encodes_haxis(), design.encodings)
    if len(haxes) == 2 and \
        haxes[0].facts == haxes[1].facts:
        design.encodings.remove(haxes[1])
    vaxes = filter(lambda x: x.encodes_vaxis(), design.encodings)
    if len(vaxes) == 2 and \
        vaxes[0].facts == vaxes[1].facts:
        design.encodings.remove(vaxes[1])

def mark_composition(design):
    marks = filter(lambda x: x.encodes_marks(), design.encodings)
    mismatch = False
    if len(marks) > 1:
        match = marks[0]
        for mark in marks:
            if not mark.facts.domain == match.facts.domain:
                mismatch = True
    if not mismatch:
        for mark in marks[1:]:
            design.encodings.remove(mark)

def compose(designs):
    if len(designs) == 2:
        new_design = Design(designs[0].encodings + designs[1].encodings)
        double_axes_composition(new_design)
        single_axis_composition(new_design)
        mark_composition(new_design)
        return new_design if not new_design.contains_conflicting_encodings() else None
    left = compose(designs[:2])
    if left:
        return compose([left] + designs[2:])

class Design(object):
    
    def __init__(self, encodings):
        self.encodings = encodings
        self.language = encodings[0].language # FIXME

    def contains_conflicting_encodings(self):
        marks = filter(lambda x: x.encodes_marks(), self.encodings)
        haxes = filter(lambda x: x.encodes_haxis(), self.encodings)
        vaxes = filter(lambda x: x.encodes_vaxis(), self.encodings)
        color = filter(lambda x: x.encodes_color(), self.encodings)
        return len(marks) > 1 or len(haxes) > 1 or len(vaxes) > 1 or len(color) > 1

    def __repr__(self):
        return "\n\t".join([str(e) for e in self.encodings])

