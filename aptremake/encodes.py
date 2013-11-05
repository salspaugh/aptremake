
from collections import defaultdict

class Encodes(object):
    
    def __init__(self, objects, facts, language):
        self.objects = objects
        self.facts = facts
        self.language = language

    def encodes_haxis(self):
        # TODO
        return False
    
    def encodes_vaxis(self):
        # TODO
        return False

def double_axes_composition(encodings):
    haxes = filter(lambda x: x.encodes_haxis(), encodings)
    vaxes = filter(lambda x: x.encodes_vaxis(), encodings)
    if len(haxes) == 2 and len(vaxes) == 2 and \
        haxes.facts.domain == haxes.facts.domain and \
        vaxes.facts.domain == vaxes.facts.domain:
        encodes.remove(haxes[1])
        encodes.remove(vaxes[1])
        # TODO: Adjust marks to differentiate them 

def single_axis_composition(encodings):
    haxes = filter(lambda x: x.encodes_haxis(), encodings)
    if len(haxes) == 2 and \
        haxes.facts.domain == haxes.facts.domain and \
        encodes.remove(haxes[1])
    vaxes = filter(lambda x: x.encodes_vaxis(), encodings)
    if len(vaxes) == 2 and \
        vaxes.facts.domain == vaxes.facts.domain:
        encodes.remove(vaxes[1])

def mark_composition(encodings):
    # TODO
    pass

class Design(object):
    
    def __init__(self, encodings):
        self.encodings = encodings

    def contains_conflicting_encodings(self):
        haxes = filter(lambda x: x.encodes_haxis(), encodings)
        vaxes = filter(lambda x: x.encodes_vaxis(), encodings)
        color = filter(lambda x: x.encodes_color(), encodings)
        return haxes > 1 or vaxes > 1 or color > 1:

    def compose(self, other):
        new_design = Design(self.encodings + other.encodings)
        double_axes_composition(encodings)
        single_axis_composition(encodings)
        mark_composition(encodings)
        if not new_design.contains_conflicting_encodings():
            return new_design
