
import json

class Type(object):

    nominal = "NOMINAL"
    quantitative = "QUANTITATIVE"
    ordinal = "ORDINAL"
    location = "LOCATION"

class Relation(object):
    
    def __init__(self, name=""): # FIXME: Make name required
        self.name = name
        self.data = []
        self.selected = False # FIXME: These attributes are tied to the
        self.importance = -1 # visualization rendering and probably shouldn't be here.

class Set(Relation):
    
    def __init__(self, name=""):
        self.tuples = None
        self.arity = None
        self.type = None
        self.domain = None
        self.determinant = self
        self.dependent = self # TODO: Verify that this isn't some awful bastard thing to do.
        Relation.__init__(self, name=name)

    def __repr__(self):
        return " ".join(["Set:", self.name, "(type: ", str(self.type) + ")"])

class FunctionalDependency(Relation):
    
    def __init__(self, name=""):
        self.determinant = None
        self.dependent = None
        self.arity = None
        self.tuples = None
        Relation.__init__(self, name=name)

    def __repr__(self):
        return " ".join(["FunctionalDependency:", self.name, "(determinant:", str(self.determinant), "dependent:", str(self.dependent) + ")"])

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
                data[s["name"]].determinant = data[s["domain"]]
                data[s["name"]].dependent = data[s["range"]]
    return data

def load(columns):
    db = connect(apt.database)
    statement = " ".join(["SELECT", "%s, "*(len(columns)+1), "FROM ", apt.table])
    columns = ["APTREMAKEID"] + columns
    statement = statement % columns
    cursor = db.execute(statement)
    data = [dict(zip(columns, tup)) for tup in cursor.fetchall()]
    db.close()
    return data
