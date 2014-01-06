
from metadata import read_metadata, Relation
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

def test(): # TODO: FIXME
    metadata = read_metadata("/Users/salspaugh/classes/visualization/project/aptremake/specs/json/cars.spec")
    #apt_input = [metadata["Car mileage for 1979"], metadata["Car price for 1979"], metadata["Car nationality for 1979"]]
    #apt_input = [metadata["Car mileage for 1979"], metadata["Repair record for 1979"]]
    #apt_input = [metadata["Car weight for 1979"], metadata["Car mileage for 1979"], metadata["Car nationality for 1979"]]
    #apt_input = [metadata["Car nationality for 1979"], metadata["Car mileage for 1979"]]
    #apt_input = [metadata["Car weight for 1979"], metadata["Car mileage for 1979"]]
    #apt_input = [metadata["Car weight for 1979"], metadata["Car nationality for 1979"], metadata["Repair record for 1979"]]
    apt_input = [metadata["Repair record for 1979"], metadata["Car nationality for 1979"], metadata["Car weight for 1979"]]
    selection_metadata = [s.name for s in apt_input]
    selection_metadata = zip(selection_metadata, range(1, len(selection_metadata)+1))
    selection_metadata = [{"name": s, "importance": i} for (s, i) in selection_metadata]
    return generate_presentation(apt_input), selection_metadata

if __name__ == "__main__":
   presentation, selection_metadata = test()
   print presentation
