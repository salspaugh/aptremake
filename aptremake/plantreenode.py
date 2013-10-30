

class PlanTreeNode(object):

    def __init__(self):
        self.parent = None
        self.children = []

    def generate_children(self):
        pass

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
