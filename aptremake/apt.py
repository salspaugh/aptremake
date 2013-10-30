
from plantreenode import PlanTreeNode

def generate_presentation(data):
    plan = PlanTreeNode()
    stack = [plan]
    while len(stack) > 0:
        plan = stack.pop(0)
        if isinstance(plan) == PresentationTreeNode:
            return PresentationTreeNode.presentation
        plan.generate_children()
        stack = plan.children + stack
