

class PlanTreeNode(object):

    def __init__(self, data):
        """
        Input:
        * data: a list of Relation objects
        """
        self.parent = None
        self.children = []
        self.data = data
    
    def add_child(self, child):
        self.children.append(child)
        child.parent = self
    
    def add_children(self, children):
        for child in children:
            self.add_child(child)

    def generate_children(self):
        """
        Note(salspaugh): I believe that if only sets of relations could be 
        partitioned, there would be only one valid partitioning, and that 
        would be that which partitioned the set of relations into subsets such
        that each subset contains exactly one of the relations. However, 
        according to the paper, it is possible for relations to be partitioned.
        We leave the implementation of that to future work.
        """
        partition = [(d,) for d in data]
        p = PartitionTreeNode(partition)
        self.add_child(p)

class PartitionTreeNode(PlanTreeNode):
    
    def __init__(self):
        self.partition = None

class SelectionTreeNode(PlanTreeNode):

    def __init__(self):
        self.selection = None

class CompositionTreeNode(PlanTreeNode):

    def __init__(self):
        pass

class PresentationTreeNode(PlanTreeNode):

    def __init__(self):
        pass
