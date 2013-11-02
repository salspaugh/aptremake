

class Type(object):

    nominal = "NOMINAL"
    quantitative = "QUANTITATIVE"
    ordinal = "ORDINAL"
    location = "LOCATION"

class Relation(object):
    
    def __init__(self, name=""):
        self.name = name

class Set(Relation):
    
    def __init__(self, name=""):
        self.data = None
        self.type = None
        Relation.__init__(self, name=name)

    def __repr__(self):
        return " ".join(["Set:", self.name, "(type: ", str(self.type) + ")"])

class FunctionalDependency(Relation):
    
    def __init__(self, name=""):
        self.domain = None
        self.range = None
        Relation.__init__(self, name=name)

    def __repr__(self):
        return " ".join(["FunctionalDependency:", self.name, "(domain:", str(self.domain), "range:", str(self.range) + ")"])

class CartesianProduct(Relation):
    
    def __init__(self, name=""):
        self.sets = None
        Relation.__init__(self, name=name)

    def __repr__(self):
        return " ".join(["CartesianProduct:", self.name, "(sets:", str(self.sets) + ")"])
