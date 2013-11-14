
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
    apt_input = [data["Car price for 1979"], data["Car mileage for 1979"], data["Car nationality for 1979"]]
    selection_data = [s.name for s in apt_input]
    selection_data = zip(selection_data, range(len(selection_data)))
    selection_data = [{"name": s, "importance": i} for (s, i) in selection_data]
    return generate_presentation(apt_input), selection_data
