
from copy import deepcopy
from data import *

def compose(designs):
    # TODO: Verify that designs is a list of designs.
    print "--------------------------------------------------------------------"
    print "COMPOSING:"
    for d in designs:
        print d.render()
        print
    if len(designs) == 0:
        return []
    if len(designs) == 1:
        return designs[0]
    if len(designs) == 2:
        return _compose(designs[0], designs[1])
    if len(designs) > 2:
        design = _compose(designs[0], designs[1])
        return compose([design] + designs[2:]) if design else None

def _compose(designa, designb):
    if no_axes(designa) or no_axes(designb):
        return merge_subplots(designa, designb)
    haxes_match = horizontal_axes_match(designa, designb)
    vaxes_match = vertical_axes_match(designa, designb)
    if haxes_match and vaxes_match:
        return merge_subplots(designa, designb)
    if haxes_match and not no_vaxes(designa) and not no_vaxes(designb):
        return concat_subplots_below(designa, designb)
    if vaxes_match and not no_haxes(designa) and not no_haxes(designb):
        return concat_subplots_right(designa, designb)

def no_haxes(design):
    return all([not s.haxis for s in design.subplots.itervalues()])

def no_vaxes(design):
    return all([not s.vaxis for s in design.subplots.itervalues()])

def no_axes(design):
    return no_haxes(design) and no_vaxes(design)

def horizontal_axes_match(designa, designb):
    # TODO: Check that not checking if permutations match is ok.
    if no_haxes(designa) and no_haxes(designb):
        return False
    ncols = designa.ncols
    if designb.ncols != ncols:
        return False
    return all([designa.haxes[i] == designb.haxes[i] for i in range(ncols)])

def vertical_axes_match(designa, designb):
    # TODO: Check that not checking if permutations match is ok.
    if no_vaxes(designa) and no_vaxes(designb):
        return False
    nrows = designa.nrows
    if designb.nrows != nrows:
        return False
    return all([designa.vaxes[i] == designb.vaxes[i] for i in range(nrows)])

def merge_subplots(designa, designb):
    if not (designa.color and designb.color and designa.color != designb.color):
        new_design= deepcopy(designa) if len(designa.subplots) > 0 else deepcopy(designb)
        new_design.color = designa.color if designa.color else designb.color
        # TODO: Make multi-mark plots work
        #for (idx, subplot) in designa.subplots.iteritems():
        #    subplot.marks.append(designb.subplots[idx])
        new_design.data = list(set(designa.data + designb.data))
        return new_design

def concat_subplots_below(designa, designb):
    if not (designa.color and designb.color and designa.color != designb.color):
        new_design= deepcopy(designa)
        new_design.color = designa.color if designa.color else designb.color
        for (idx, subplot) in designb.subplots.iteritems():
            new_subplot = deepcopy(subplot)
            (r,c) = idx
            new_subplot.ridx += new_design.nrows
            new_design.subplots[(r+new_design.nrows, c)] = new_subplot
        new_design.nrows += designb.nrows
        new_design.data = list(set(designa.data + designb.data))
        return new_design
    
def concat_subplots_right(designa, designb):
    if not (designa.color and designb.color and designa.color != designb.color):
        new_design= deepcopy(designa)
        new_design.color = designa.color if designa.color else designb.color
        for (idx, subplot) in designb.subplots.iteritems():
            new_subplot = deepcopy(subplot)
            (r,c) = idx
            new_subplot.cidx += new_design.ncols
            new_design.subplots[(r, c+new_design.ncols)] = new_subplot
        new_design.ncols += designb.ncols
        new_design.data = list(set(designa.data + designb.data))
        return new_design
    


