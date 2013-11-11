
from data import read_data
from plantree import RootNode, PresentationTreeNode

def generate_presentation(data):
    plan = RootNode(data)
    stack = [plan]
    while len(stack) > 0:
        node = stack.pop(0)
        if isinstance(node, PresentationTreeNode):
            return node.presentation
        node.generate_children()
        stack = node.children + stack

def test():
    data = read_data("/Users/salspaugh/classes/visualization/project/aptremake/data/cars.spec")
    return generate_presentation([data["Car price for 1979"], data["Car mileage for 1979"]])

test()

