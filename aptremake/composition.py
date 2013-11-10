
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

def encode_marks_differently(design):
    marks = filter(lambda x: x.encodes_marks(), design.encodings)
    marks_facts_names = [mark.facts.name for mark in marks]
    if len(set(marks_facts_names)) > 1:
        if not design.color_assigned():
            marks_facts_names_set = Set(name="+".join(list(set(marks_facts_names))))
            marks_facts_names_set.data = set(marks_facts_names)
            marks_facts_names_set.name = Type.nominal
            marks_facts_names_set.domain = "Mark Names"
            design.encodings.add(Color.design(relation_set))

def double_axes_composition(design):
    haxes = filter(lambda x: x.encodes_haxis(), design.encodings)
    vaxes = filter(lambda x: x.encodes_vaxis(), design.encodings)
    if len(haxes) == 2 and len(vaxes) == 2 and \
        haxes[0].facts.domain == haxes[1].facts.domain and \
        vaxes[0].facts.domain == vaxes[1].facts.domain:
        design.encodings.remove(haxes[1])
        design.encodings.remove(vaxes[1])
        encode_marks_differently(design)

def single_axis_composition(design):
    haxes = filter(lambda x: x.encodes_haxis(), design.encodings)
    if len(haxes) == 2 and \
        haxes[0].facts.domain == haxes[1].facts.domain:
        design.encodings.remove(haxes[1])
        encode_marks_differently(design)
    vaxes = filter(lambda x: x.encodes_vaxis(), design.encodings)
    if len(vaxes) == 2 and \
        vaxes[0].facts.domain == vaxes[1].facts.domain:
        design.encodings.remove(vaxes[1])
        encode_marks_differently(design)

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
        self.language = encodings[0].language # FIXME:
        # What happens when encodings have a mix of languages.

    def __repr__(self):
        return "\n\t".join([str(e) for e in self.encodings])

    def hpos(self):
        for encoding in self.encodings:
            if encoding.objects == Objects.hpos:
                return encoding

    def vpos(self):
        for encoding in self.encodings:
            if encoding.objects == Objects.vpos:
                return encoding

    def color(self):
        for encoding in self.encodings:
            if encoding.objects == Objects.color:
                return encoding

    def contains_conflicting_encodings(self):
        haxes = filter(lambda x: x.encodes_haxis(), self.encodings)
        vaxes = filter(lambda x: x.encodes_vaxis(), self.encodings)
        color = filter(lambda x: x.encodes_color(), self.encodings)
        return len(haxes) > 1 or len(vaxes) > 1 or len(color) > 1
