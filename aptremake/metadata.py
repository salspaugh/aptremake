
import json
from sqlite3 import connect

store = {}

class Type(object):

    nominal = "nominal"
    quantitative = "quantitative"
    ordinal = "ordinal"
    location = "location"

class Relation(object):
    
    def __init__(self, name=""): # FIXME: Make name required
        self.name = name
        self.selected = False # FIXME: These attributes are tied to the
        self.importance = -1 # visualization rendering and probably shouldn't be here.

class Set(Relation):
    
    def __init__(self, name=""):
        self.arity = None
        self.type = None
        self.domain = None
        self.ordering = None 
        self.determinant = self # This is kludgy.
        self.dependent = self 
        Relation.__init__(self, name=name)

    def __repr__(self):
        return " ".join(["<Set:", self.name, "(type: ", str(self.type) + ")>"])

class FunctionalDependency(Relation):
    
    def __init__(self, name=""):
        self.determinant = None
        self.dependent = None
        self.arity = None
        Relation.__init__(self, name=name)

    def __repr__(self):
        return " ".join(["<FunctionalDependency:", self.name, "(determinant:", str(self.determinant), "dependent:", str(self.dependent) + ")>"])

class CartesianProduct(Relation):
    
    def __init__(self, name=""):
        self.independent = None
        self.dependent = None
        self.arity = None
        Relation.__init__(self, name=name)

    def __repr__(self):
        return " ".join(["<CartesianProduct:", self.name, "(sets:", str(self.sets) + ")>"])

classes = {
    "Set": Set, 
    "FunctionalDependency": FunctionalDependency,
    "CartesianProduct": CartesianProduct
}

def validate(relation):
    if isinstance(relation, FunctionalDependency):
        if not relation.determinant:
            raise AttributeError("Attribute 'determinant' not set.")
        if not relation.dependent:
            raise AttributeError("Attribute 'dependent' not set.")
    if isinstance(relation, Set):
        if not relation.domain:
            raise AttributeError("Attribute 'domain' not set.")
        if not relation.type:
            raise AttributeError("Attribute 'type' not set.")
    if not relation.arity:
        raise AttributeError("Attribute 'arity' not set.")
    raise AttributeError("Invalid input type (must be FunctionalDependency or Set).") 

def read_metadata(specfilename):
    metadata = {}
    with open(specfilename) as specfile:
        spec = json.load(specfile)
        metadatabase = spec["metadatabase"]
        query = spec["query"]
        for s in spec["relations"]:
            d = classes[s["class"]](name=s["name"])
            d.type = s.get("type", None)
            d.domain = s.get("domain", None)
            d.ordering = s.get("ordering", None)
            d.arity = s["arity"]
            metadata[s["name"]] = d
        for s in spec["relations"]:
            if s["class"] == "FunctionalDependency":
                d = metadata[s["name"]]
                d.determinant = metadata[s["determinant"]]
                d.dependent = metadata[s["dependent"]]
                d.metadata = [d.determinant.name, d.dependent.name]
    return metadata

def load(database, query, labels):
    db = connect(database)
    cursor = db.execute(query)
    data = [dict(zip(labels, tup)) for tup in cursor.fetchall()]
    db.close()
    return data
