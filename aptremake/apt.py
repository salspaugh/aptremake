
from metadata import read_metadata, validate, Relation
from plantree import RootNode, PresentationTreeNode

def generate_presentation(database, metadata, query, labels, limit=5):
    for relation in metadata:
        validate(relation)
    count = 0
    plan = RootNode(database, metadata, query, labels)
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
