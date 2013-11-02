
from data import FunctionalDependency, Set, Type
from plantree import RootNode, PresentationTreeNode

def generate_presentation(data):
    plan = RootNode(data)
    stack = [plan]
    while len(stack) > 0:
        node = stack.pop(0)
        if isinstance(node, PresentationTreeNode):
            return PresentationTreeNode.presentation
        node.generate_children()
        stack = node.children + stack
    plan.print_tree()

def test():
    cars = Set(name="Cars")
    cars.type = Type.nominal

    price = Set()
    price.type = Type.quantitative
    pricefd = FunctionalDependency(name="Price")
    pricefd.domain = cars
    pricefd.range = price

    mileage = Set()
    mileage.type = Type.quantitative
    mileagefd = FunctionalDependency(name="Mileage")
    mileagefd.domain = cars
    mileagefd.range = mileage

    weight = Set()
    weight.type = Type.quantitative
    weightfd = FunctionalDependency(name="Weight")
    weightfd.domain = cars
    weightfd.range = weight
    
    repair = Set()
    repair.type = Type.ordinal
    repairfd = FunctionalDependency(name="Repair")
    repairfd.domain = cars
    repairfd.range = repair
    
    nation = Set()
    nation.type = Type.nominal
    nationfd = FunctionalDependency(name="Nation")
    nationfd.domain = cars
    nationfd.range = nation
   
    generate_presentation([pricefd, mileagefd, repairfd, weightfd])

test()
