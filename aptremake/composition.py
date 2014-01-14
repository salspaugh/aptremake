
from copy import deepcopy
from metadata import *
from design import *
from logging import basicConfig, debug, DEBUG

basicConfig(filename='aptremake.log', level=DEBUG)

def compose(designs):
    # TODO: Verify that designs is a list of designs.
    debug("--------------------------------------------------------------------")
    debug("COMPOSING:")
    for d in designs:
        debug(d)
    if len(designs) == 0:
        return []
    if len(designs) == 1:
        return designs[0]
    if len(designs) == 2:
        return _compose(designs[0], designs[1])
    if len(designs) > 2:
        design = _compose(designs[0], designs[1])
        return compose([design] + designs[2:]) if design else None

def _compose(designa, designb): # TODO: Document pre-conditions for functions
    if retinal_encodings_conflict(designa, designb):
        return None
    if not has_axes(designa) or not has_axes(designb):
        return merge_matching_axes(designa, designb)
    haxes_match = horizontal_axes_match(designa, designb)
    vaxes_match = vertical_axes_match(designa, designb)
    if haxes_match and vaxes_match:
        return merge_matching_axes(designa, designb)
    if haxes_match and has_vaxes(designa) and has_vaxes(designb):
        return concat_subplots_below(designa, designb)
    if vaxes_match and has_haxes(designa) and has_haxes(designb):
        return concat_subplots_right(designa, designb)
    if axes_compatible(designa, designb):
        return merge_compatible_axes(designa, designb)

def retinal_encodings_conflict(designa, designb):
    return (designa.color and designb.color and designa.color != designb.color)

def has_haxes(design):
    return any([s.haxis for s in design.subplots.itervalues()])

def has_vaxes(design):
    return any([s.vaxis for s in design.subplots.itervalues()])

def has_axes(design):
    return has_haxes(design) or has_vaxes(design)

def horizontal_axes_match(designa, designb):
    if not has_haxes(designa) or not has_haxes(designb):
        return False
    ncols = designa.ncols
    if designb.ncols != ncols:
        return False
    return all([designa.haxes[i] == designb.haxes[i] for i in range(ncols)])

def vertical_axes_match(designa, designb):
    if not has_vaxes(designa) or not has_vaxes(designb):
        return False
    nrows = designa.nrows
    if designb.nrows != nrows:
        return False
    return all([designa.vaxes[i] == designb.vaxes[i] for i in range(nrows)])

def axes_compatible(designa, designb):
    if designa.nrows != designb.nrows or designa.ncols != designb.ncols:
        return False
    for (idx, subplota) in designa.subplots.iteritems():
        subplotb = designb.subplots[idx]
        compatible = (subplota.haxis and not subplotb.haxis and not subplota.vaxis and subplotb.vaxis) or \
                    (not subplota.haxis and subplotb.haxis and subplota.vaxis and not subplotb.vaxis)
        if not (compatible and subplota.marks.metadata == subplotb.marks.metadata):
            return False
    return True

def merge_compatible_axes(designa, designb):
    debug("Merging compatible axes")
    new_design = deepcopy(designa)
    new_design.copy_color(designa) if designa.color else new_design.copy_color(designb)
    new_design.haxes = (deepcopy(designa.haxes) if len(designb.haxes) == 0 else deepcopy(designb.haxes))
    new_design.vaxes = (deepcopy(designa.vaxes) if len(designb.vaxes) == 0 else deepcopy(designb.vaxes))
    for (idx, subplota) in designa.subplots.iteritems():
        subplotb = designb.subplots[idx]
        new_subplot = Subplot(deepcopy(subplota.marks))
        new_subplot.copy_haxis(subplota) if subplota.haxis else new_subplot.copy_haxis(subplotb) 
        new_subplot.copy_vaxis(subplota) if subplota.vaxis else new_subplot.copy_vaxis(subplotb) 
        new_design.subplots[idx] = new_subplot
    return new_design

def merge_matching_axes(designa, designb):
    debug("Merging matching axes")
    new_design = deepcopy(designa) if len(designa.subplots) > 0 else deepcopy(designb)
    new_design.copy_color(designa) if designa.color else new_design.copy_color(designb)
    # TODO: Make multi-mark plots work
    #for (idx, subplot) in designa.subplots.iteritems():
    #    subplot.marks.append(designb.subplots[idx])
    return new_design

def concat_subplots_below(designa, designb):
    debug("Concatenating subplots below")
    new_design = deepcopy(designa)
    new_design.copy_color(designa) if designa.color else new_design.copy_color(designb)
    for (idx, subplot) in designb.subplots.iteritems():
        new_subplot = deepcopy(subplot)
        (r,c) = idx
        new_subplot.ridx += new_design.nrows
        new_design.subplots[(r+new_design.nrows, c)] = new_subplot
    new_design.nrows += designb.nrows
    return new_design
    
def concat_subplots_right(designa, designb):
    debug("Concatenating subplots right")
    new_design = deepcopy(designa)
    new_design.copy_color(designa) if designa.color else new_design.copy_color(designb)
    for (idx, subplot) in designb.subplots.iteritems():
        new_subplot = deepcopy(subplot)
        (r,c) = idx
        new_subplot.cidx += new_design.ncols
        new_design.subplots[(r, c+new_design.ncols)] = new_subplot
    new_design.ncols += designb.ncols
    return new_design
    
