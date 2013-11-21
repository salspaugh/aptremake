
from collections import defaultdict, OrderedDict
from data import *


class Objects(object):
    
    marks = "MARKS"
    haxis = "HAXIS"
    vaxis = "VAXIS"
    hpos = "HPOS"
    vpos = "VPOS"
    color = "COLOR"
    height = "HEIGHT" # vertical length
    width = "WIDTH" # horizontal length
    marktype = "MARKTYPE"


class Encodes(object):
    
    def __init__(self, objects, facts, language):
        self.objects = objects
        self.facts = facts
        self.language = language

    def encodes(self, objects):
        return self.objects == objects

    def encodes_marks(self):
        return self.encodes(Objects.marks)

    def encodes_haxis(self):
        return self.encodes(Objects.haxis)

    def encodes_vaxis(self):
        return self.encodes(Objects.vaxis)

    def encodes_hpos(self):
        return self.encodes(Objects.hpos)

    def encodes_vpos(self):
        return self.encodes(Objects.vpos)

    def encodes_color(self):
        return self.encodes(Objects.color)

    def encodes_marktype(self):
        return self.encodes(Objects.marktype)

    def __repr__(self):
        return "Encodes(%s, %s, %s)" % (self.objects, self.facts, self.language)


class Design(object):
    
    def __init__(self, encodings, tasks):
        self.encodings = encodings
        self.tasks = tasks

    def __repr__(self):
        return "DESIGN: " + "\n\t".join([str(e) for e in self.encodings])

    def axes(self):
        return filter(lambda x: x.encodes_haxis() or x.encodes_vaxis(), self.encodings)

    def haxes(self): 
        return filter(lambda x: x.encodes_haxis(), self.encodings)

    def vaxes(self): 
        return filter(lambda x: x.encodes_vaxis(), self.encodings)

    def positions(self):
        return filter(lambda x: x.encodes_hpos() or x.encodes_vpos(), self.encodings)
    
    def hpos(self): 
        return filter(lambda x: x.encodes_hpos(), self.encodings)

    def vpos(self):
        return filter(lambda x: x.encodes_vpos(), self.encodings)

    def color(self):
        return filter(lambda x: x.encodes_color(), self.encodings)

    def marks(self):
        return filter(lambda x: x.encodes_marks(), self.encodings)

    def marktype(self):
        m = filter(lambda x: x.encodes_marktype(), self.encodings)
        if len(m) == 0:
            return "dot"
        if len(m) == 1:
            return m[0].facts
        if len(m) > 1:
            raise Exception # TODO: Make a not yet implemented error.

    def remove_duplicate_axes(self):
        haxes = defaultdict(list)
        for haxis in self.haxes():
            haxes[haxis.facts.domain].append(haxis)
        for (domain, axis) in haxes.iteritems():
            for a in axis[1:]:
                self.encodings.remove(a)
        vaxes = defaultdict(list)
        for vaxis in self.vaxes():
            vaxes[vaxis.facts.domain].append(vaxis)
        for (domain, axis) in vaxes.iteritems():
            for a in axis[1:]:
                self.encodings.remove(a)

    def contains_conflicting_encodings(self):
        haxes = filter(lambda x: x.encodes_haxis(), self.encodings)
        vaxes = filter(lambda x: x.encodes_vaxis(), self.encodings)
        color = filter(lambda x: x.encodes_color(), self.encodings)
        return len(haxes) > 1 or len(vaxes) > 1 or len(color) > 1

def _merge_tasks(designa, designb):
    tasks = OrderedDict()
    for (k,v) in designa.tasks.iteritems():
        tasks[k] = v
    for (k,v) in designb.tasks.iteritems():
        if not k in tasks:
            tasks[k] = v
    return tasks

def _color_conflict(designa, designb):
    colora = designa.color()
    colorb = designb.color()
    if len(colora) > 1 or len(colorb) > 1:
        return True
    if len(colora) == len(colorb) == 1:
        domaina = colora[0].facts.dependent.domain
        domainb = colorb[0].facts.dependent.domain
        return not domaina == domainb
    return False

def _compose_marks(designa, designb):
    marks_domains = [d.facts.domain for d in designa.marks() + designb.marks()] 
    if _color_conflict(designa, designb):
        return None
    if len(set(marks_domains)) == 1:
        encodings = designa.encodings + filter(lambda x: not x.encodes_marks(), designb.encodings)
        tasks = _merge_tasks(designa, designb)
        return Design(encodings, tasks)
    return None

def _compose_double_axes(designa, designb):
    raise Exception # TODO: Make a not yet implemented error.

def _compose_single_axes(designa, designb): # TODO: Test this.
    haxes_matches = defaultdict(list)
    for axis in designa.haxes() + designb.haxes():
        haxes_matches[axis.facts.domain].append(axis)
    all_haxes_match = all([len(axes) == 2 for (domain, axes) in haxes_matches.iteritems()])
    vaxes_matches = defaultdict(list)
    for axis in designa.vaxes() + designb.vaxes():
        vaxes_matches[axis.facts.domain].append(axis)
    all_vaxes_match = all([len(axes) == 2 for (domain, axes) in vaxes_matches.iteritems()])
    if (all_haxes_match and not all_vaxes_match) or (not all_haxes_match and all_vaxes_match):
        encodings = designa.encodings + designb.encodings
        tasks = _merge_tasks(designa, designb)
        d = Design(encodings, tasks)
        d.remove_duplicate_axes()
        return d
    if all_haxes_match and all_vaxes_match:
        return _compose_double_axes(designa, designb)
    return None
    

def _compose(designa, designb):
    ha = designa.hpos()
    va = designa.vpos()
    hb = designb.hpos()
    vb = designb.vpos()

    """Sixteen possible cases:"""
    """(0) Neither design encodes position so that means they both encode color."""
    if not ha and not va and not hb and not vb:
        return None # TODO: Update this later when more encodings are added.

    """(1) One design encodes one position and the other encodes color."""
    if not ha and not va and not hb and vb:
        return _compose_marks(designa, designb)

    """(2) One design encodes one position and the other encodes color."""
    if not ha and not va and hb and not vb:
        return _compose_marks(designa, designb)

    """(3) One design encodes both positions and the other encodes color."""
    if not ha and not va and hb and vb:
        return _compose_marks(designa, designb)

    """(4) One design encodes one position and the other encodes color."""
    if not ha and va and not hb and not vb:
        return _compose_marks(designa, designb)

    """(5) One design has both axes defined and the other only has one."""
    if not ha and va and not hb and vb:
        return None # TODO: Test that this is okay.

    """(6) Designs encode opposite positions."""
    if not ha and va and hb and not vb:
        return _compose_marks(designa, designb)

    """(7) One design has both axes defined and the other only has one."""
    if not ha and va and hb and vb:
        return _compose_single_axes(designa, designb)

    """(8) One design encodes one position and the other encodes color."""
    if ha and not va and not hb and not vb:
        return _compose_marks(designa, designb)

    """(9) Designs encode opposite positions."""
    if ha and not va and not hb and vb:
        return _compose_marks(designa, designb)

    """(10) One design has both axes defined and the other only has one."""
    if ha and not va and hb and not vb:
        return None # TODO: Test that this is okay.

    """(11) One design has both axes defined and the other only has one."""
    if ha and not va and hb and vb:
        return _compose_single_axes(designa, designb)

    """(12) One design encodes both positions and the other encodes color."""
    if ha and va and not hb and not vb:
        return _compose_marks(designa, designb)

    """(13) One design has both axes defined and the other only has one."""
    if ha and va and not hb and vb:
        return _compose_single_axes(designa, designb)

    """(14) One design has both axes defined and the other only has one."""
    if ha and va and hb and not vb:
        return _compose_single_axes(designa, designb)

    """(15) Both designs have both horizontal and vertical axes defined."""
    if ha and va and hb and vb:
        if len(ha) == len(hb) == len(va) == len(vb) == 1:
            haxes_match = (ha[0].facts.dependent.domain == hb[0].facts.dependent.domain)
            vaxes_match = (va[0].facts.dependent.domain == vb[0].facts.dependent.domain)
            if haxes_match and vaxes_match:
                encodings = designa.encodings + designb.marks() + designb.color()
                tasks = _merge_tasks(designa, designb)
                design = Design(encodings, tasks)
                if not design.color(): # TODO: Test this
                    marks_set = Set()
                    marks_set.data = [d.facts.name for d in design.marks()]
                    marks_set.type = Type.nominal
                    marks_set.domain = "Mark Names" # FIXME
                    design.encodings.append(Color.design(marks_set))
                else:
                    return None
            elif (not haxes_match and vaxes_match) or (haxes_match and not vaxes_match):
                encodings = designa.encodings + designb.encodings
                tasks = _merge_tasks(designa, designb)
                return Design(encodings, tasks)
            else: # Neither horizontal nor vertical axes match.
                return None
        return None # TODO: Deal with other cases.

def compose(designs):
    # TODO: Verify that designs is a list of designs.
    print
    for d in designs:
        print d
    if len(designs) == 0:
        return []
    if len(designs) == 1:
        return designs[0]
    if len(designs) == 2:
        return _compose(designs[0], designs[1])
    if len(designs) > 2:
        design = _compose(designs[0], designs[1])
        return compose([design] + designs[2:]) if design else None
    return None
