
import json

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
        self.tuples = None
        self.arity = None
        self.type = None
        self.domain = None
        Relation.__init__(self, name=name)

    def __repr__(self):
        return " ".join(["Set:", self.name, "(type: ", str(self.type) + ")"])

class FunctionalDependency(Relation):
    
    def __init__(self, name=""):
        self.domain = None
        self.range = None
        self.arity = None
        self.tuples = None
        Relation.__init__(self, name=name)

    def __repr__(self):
        return " ".join(["FunctionalDependency:", self.name, "(domain:", str(self.domain), "range:", str(self.range) + ")"])

class CartesianProduct(Relation):
    
    def __init__(self, name=""):
        self.independent = None
        self.dependent = None
        self.arity = None
        self.tuples = None
        Relation.__init__(self, name=name)

    def __repr__(self):
        return " ".join(["CartesianProduct:", self.name, "(sets:", str(self.sets) + ")"])

classes = {
    "Set": Set, 
    "FunctionalDependency": FunctionalDependency,
    "CartesianProduct": CartesianProduct
}

def read_data(specfilename):
    data = {}
    with open(specfilename) as specfile:
        spec = json.load(specfile)
        for s in spec:
            d = classes[s["class"]](name=s["name"])
            d.type = s.get("type", None)
            d.domain = s.get("domain", None)
            d.tuples = s["data"]
            d.arity = s["arity"]
            data[s["name"]] = d
        for s in spec:
            if s["class"] == "FunctionalDependency":
                data[s["name"]].domain = data[s["domain"]]
                data[s["name"]].range = data[s["range"]]
    return data
