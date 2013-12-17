
from data import Relation
from languages import _languages
from ranking import rank
from composition import compose

INDENT = '    '

class PlanTreeNode(object):

    def __init__(self):
        self.parent = None
        self.children = []
    
    def add_child(self, child):
        self.children.append(child)
        child.parent = self
    
    def add_children(self, children):
        for child in children:
            self.add_child(child)
    
    def flatten(self, container):
        for i in container:
            if isinstance(i, list) or isinstance(i, tuple):
                for j in self.flatten(i):
                    yield j
            else:
                yield i

    def _str_tree(self, recursive=True, indent=1):
        to_str = str(self)
        to_str = ''.join([to_str])
        if recursive:
            for child in self.children:
                to_str = ''.join([to_str, '\n', INDENT*indent, child._str_tree(indent=indent+1)])
        return to_str

    def str_tree(self, recursive=True):
        return self._str_tree(recursive=recursive)

    def print_tree(self, recursive=True):
        print self.str_tree(recursive=recursive)

class RootNode(PlanTreeNode):

    def __init__(self, data):
        """
        Input:
        * data: a list of Relation objects
        """
        if not isinstance(data, list):
            raise AttributeError("Data argument must be a list.")
        if not all([isinstance(d, Relation) for d in data]):
            raise AttributeError("Data argument list must only contain Relation objects.")
        self.data = data
        PlanTreeNode.__init__(self)

    def generate_children(self):
        """
        Note(salspaugh): I believe that if only sets of relations could be 
        partitioned, there would be only one valid partitioning, and that 
        would be that which partitioned the set of relations into subsets such
        that each subset contains exactly one of the relations. However, 
        according to the paper, it is possible for relations to be partitioned.
        We leave the implementation of that to future work.
        """
        p = PartitionTreeNode(self.data)
        self.add_child(p)

    def __repr__(self):
        return " ".join(["DATA:", str(self.data)])

class PartitionTreeNode(PlanTreeNode):
    
    def __init__(self, partition):
        self.partition = partition
        PlanTreeNode.__init__(self) 

    def combine(self, sets): # TODO: Replace with itertools version
        if len(sets) == 0:
            return sets
        if len(sets) == 1:
            return [[s] for s in sets[0]]
        combined = []
        if len(sets) == 2:
            for i in sets[0]:
                for j in sets[1]:
                    combined.append((i,j))
            return combined
        return self.combine([sets[0], self.combine(sets[1:])])

    def get_designs(self, partition):
        designs = []
        for language in _languages:
            if language.can_express(partition):
                designs.append(language.design(partition))
        return rank(partition, designs)

    def generate_children(self):
        designs = []
        for part in self.partition:
            designs.append(self.get_designs(part))
        for selections in self.combine(designs):
            selections = list(self.flatten(selections))
            s = SelectionTreeNode()
            s.selections = selections
            self.add_child(s)

    def __repr__(self):
        return " ".join(["PARTITION:", str(self.partition)])

class SelectionTreeNode(PlanTreeNode):

    def __init__(self):
        self.selections = None
        PlanTreeNode.__init__(self)
    
    def generate_children(self):
        print "================================================================"
        print "TRYING:"
        print
        for s in self.selections:
            print s
            print
        design = compose(self.selections)
        if design:
            c = CompositionTreeNode(design)
            self.add_child(c)
        else:
            print "FAILED"

    def __repr__(self):
        return " ".join(["SELECTION:"] + [str(s) for s in self.selections])

class CompositionTreeNode(PlanTreeNode):

    def __init__(self, design):
        self.design = design
        PlanTreeNode.__init__(self)

    def generate_children(self):
        presentation = self.design.render()
        p = PresentationTreeNode(presentation)
        self.add_child(p)

    def __repr__(self):
        return " ".join(["COMPOSITION:", str(self.design)])

class PresentationTreeNode(PlanTreeNode):

    def __init__(self, presentation):
        self.presentation = presentation
        PlanTreeNode.__init__(self)
