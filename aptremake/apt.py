
from metadata import read_metadata, validate, Relation
from plantree import RootNode, PresentationTreeNode

def generate_presentation(view, limit=5):
    for relation in view.relations:
        validate(relation)
    count = 0
    plan = RootNode(view)
    stack = [plan]
    while len(stack) > 0:
        node = stack.pop(0)
        if isinstance(node, PresentationTreeNode):
            yield node.presentation
            count += 1
            if count == limit:
                break
        node.generate_children()
        stack = node.children + stack
