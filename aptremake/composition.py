
from collections import defaultdict, OrderedDict
from data import *


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

def _compose(designa, designb):
    haxes_match = horizontal_axes_match(designa, designb)
    vaxes_match = vertical_axes_match(designa, designb)
    if haxes_match and vaxes_match:
        return merge_subplots(designa, designb)
    if haxes_match:
        return concat_subplots_below(designa, designb)
    if vaxes_match:
        return concat_subplots_right(designa, designb)

def horizontal_axes_match(designa, designb):
    # TODO: Check that not checking if permutations match is ok.
    ncols = designa.ncols
    if designb.ncols != ncols:
        return False
    return all([designa.haxes[i] == designb.haxes[i] for i in range(ncols)]):

def vertical_axes_match(designa, designb):
    # TODO: Check that not checking if permutations match is ok.
    nrows = designa.nrows
    if designb.nrows != nrows:
        return False
    return all([designa.vaxes[i] == designb.vaxes[i] for i in range(nrows)]):

def merge_subplots(designa, designb):
    if not (designa.color and designb.color and designa.color != designb.color):
        (designb.color = designa.color) if designa.color else (designa.color = designb.color)
        for (idx, subplot) in designa.subplots.iteritems():
            subplot.marks.append(designb.subplots[idx])
        return designa

def concat_subplots_below(designa, designb):
    if not (designa.color and designb.color and designa.color != designb.color):
        (designb.color = designa.color) if designa.color else (designa.color = designb.color)
        for (idx, subplot) in designb.subplots.iteritems():
            (r,c) = idx
            subplot.rowidx += designa.nrows
            designa.subplots[(r+designa.nrows, c)] = subplot
        designa.data = list(set(designa.data + designb.data))
        return designa
    
def concat_subplots_right(designa, designb):
    if not (designa.color and designb.color and designa.color != designb.color):
        (designb.color = designa.color) if designa.color else (designa.color = designb.color)
        for (idx, subplot) in designb.subplots.iteritems():
            (r,c) = idx
            subplot.colidx += designa.ncols
            designa.subplots[(r, c+designa.ncols)] = subplot
        designa.data = list(set(designa.data + designb.data))
        return designa
    


