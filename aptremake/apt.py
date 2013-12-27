
from data import read_data
from plantree import RootNode, PresentationTreeNode

def generate_presentation(data):
    plan = RootNode(data)
    stack = [plan]
    while len(stack) > 0:
        node = stack.pop(0)
        if isinstance(node, PresentationTreeNode):
            yield node.presentation
        node.generate_children()
        stack = node.children + stack

def test():
    data = read_data("/Users/salspaugh/classes/visualization/project/aptremake/specs/json/cars.spec")
    #apt_input = [data["Car mileage for 1979"], data["Car price for 1979"], data["Car nationality for 1979"]]
    #apt_input = [data["Car mileage for 1979"], data["Repair record for 1979"]]
    #apt_input = [data["Car weight for 1979"], data["Car mileage for 1979"], data["Car nationality for 1979"]]
    #apt_input = [data["Car nationality for 1979"], data["Car mileage for 1979"]]
    #apt_input = [data["Car weight for 1979"], data["Car mileage for 1979"]]
    #apt_input = [data["Car weight for 1979"], data["Car nationality for 1979"], data["Repair record for 1979"]]
    apt_input = [data["Repair record for 1979"], data["Car nationality for 1979"], data["Car weight for 1979"]]
    selection_data = [s.name for s in apt_input]
    selection_data = zip(selection_data, range(1, len(selection_data)+1))
    selection_data = [{"name": s, "importance": i} for (s, i) in selection_data]
    return generate_presentation(apt_input), selection_data

if __name__ == "__main__":
   presentation, selection_data = test()
   print presentation
