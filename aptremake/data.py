

class Relation(object):
    
    def __init__(self):
        self.name = ""

class Set(Relation):
    
    def __init__(self):
        self.data = None
        self.type = None

class FunctionalDependency(Relation):
    
    def __init__(self):
        self.domain = None
        self.range = None

class CartesianProduct(Relation):
    
    def __init__(self):
        self.sets = None
