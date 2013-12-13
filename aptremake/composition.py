
from collections import defaultdict, OrderedDict
from data import *


def compose(designs):
    # TODO: Verify that designs is a list of designs.
    print
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
    if haxes_match:
        return concat_subplots_below(designa, designb)
    if vaxes_match:
        return concat_subplots_right(designa, designb)

def no_axes(design):
    no_haxes = all([not s.haxis for s in design.subplots.itervalues()])
    no_vaxes = all([not s.vaxis for s in design.subplots.itervalues()])
    return no_haxes and no_vaxes

def horizontal_axes_match(designa, designb):
    # TODO: Check that not checking if permutations match is ok.
    ncols = designa.ncols
    if designb.ncols != ncols:
        return False
    return all([designa.haxes[i] == designb.haxes[i] for i in range(ncols)])

def vertical_axes_match(designa, designb):
    # TODO: Check that not checking if permutations match is ok.
    nrows = designa.nrows
    if designb.nrows != nrows:
        return False
    return all([designa.vaxes[i] == designb.vaxes[i] for i in range(nrows)])

def merge_subplots(designa, designb):
    if not (designa.color and designb.color and designa.color != designb.color):
        if designa.color:
            designb.color = designa.color
        else:
            designa.color = designb.color
        # TODO: Make multi-mark plots work
        #for (idx, subplot) in designa.subplots.iteritems():
        #    subplot.marks.append(designb.subplots[idx])
        designa.data = list(set(designa.data + designb.data))
        return designa

def concat_subplots_below(designa, designb):
    if not (designa.color and designb.color and designa.color != designb.color):
        if designa.color:
            designb.color = designa.color
        else:
            designa.color = designb.color
        for (idx, subplot) in designb.subplots.iteritems():
            (r,c) = idx
            subplot.ridx += designa.nrows
            designa.subplots[(r+designa.nrows, c)] = subplot
        designa.nrows += designb.nrows
        designa.data = list(set(designa.data + designb.data))
        return designa
    
def concat_subplots_right(designa, designb):
    if not (designa.color and designb.color and designa.color != designb.color):
        if designa.color:
            designb.color = designa.color
        else:
            designa.color = designb.color
        for (idx, subplot) in designb.subplots.iteritems():
            (r,c) = idx
            subplot.cidx += designa.ncols
            designa.subplots[(r, c+designa.ncols)] = subplot
        designa.ncols += designb.ncols
        designa.data = list(set(designa.data + designb.data))
        return designa
    


