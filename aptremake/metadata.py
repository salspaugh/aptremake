
import json

from db import Database

class View(object):

    def __init__(self, relations, database, query, query_params,
                 keys, raw_features=None, caption=""):
        if not hasattr(relations, "__iter__"):
            raise AttributeError("Relations must be iterable.")
        if not all([isinstance(d, Relation) for d in relations]):
            raise AttributeError("Relations list must only contain Relation objects.")
        self.relations = relations
        self.database = database
        self.query = query
        self.query_params = query_params
        self.keys = keys
        self.raw_features = raw_features
        self.caption = caption

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
        self.label = name
        self.coding = None

class Set(Relation):
    
    def __init__(self, name=""):
        self.arity = None
        self.type = None
        self.domain = None
        self.ordering = None 
        self.determinant = self # FIXME: This is kludgy.
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
    if not relation.arity:
        raise AttributeError("Attribute 'arity' not set.")
    if isinstance(relation, FunctionalDependency):
        if not relation.determinant:
            raise AttributeError("Attribute 'determinant' not set.")
        if not relation.dependent:
            raise AttributeError("Attribute 'dependent' not set.")
    elif isinstance(relation, Set):
        if not relation.domain:
            raise AttributeError("Attribute 'domain' not set.")
        if not relation.type:
            raise AttributeError("Attribute 'type' not set.")
        return
    else:
        raise AttributeError("Invalid input type (must be FunctionalDependency or Set).") 

def read_metadata(specfilename):
    metadata = {}
    with open(specfilename) as specfile:
        spec = json.load(specfile)
        metadata["driver"] = spec["driver"]
        metadata["database"] = spec.get("database", None)
        metadata["path"] = spec.get("path", None)
        metadata["user"] = spec.get("user", None)
        metadata["password"] = spec.get("password", None)
        metadata["host"] = spec.get("host", None)
        metadata["port"] = spec.get("port", None)
        metadata["table"] = spec["table"]
        metadata["relations"] = {}
        for s in spec["relations"]:
            d = classes[s["class"]](name=s["name"])
            d.type = s.get("type", None)
            d.domain = s.get("domain", None)
            d.ordering = s.get("ordering", None)
            d.arity = s.get("arity", None)
            d.label = s.get("label", None)
            d.coding = s.get("coding", None)
            metadata["relations"][s["name"]] = d
        for s in spec["relations"]:
            if s["class"] == "FunctionalDependency":
                d = metadata["relations"][s["name"]]
                d.determinant = metadata["relations"][s["determinant"]]
                d.dependent = metadata["relations"][s["dependent"]]
    return metadata

def setup_database(metadata):
    return Database(metadata["driver"],
        path=metadata.get("path", None),
        database=metadata.get("database", None),
        user=metadata.get("user", None),
        password=metadata.get("password", None),
        host=metadata.get("host", None),
        port=metadata.get("port", None))

def load(view):
    db = view.database.connect()
    cursor = db.execute(view.query, view.query_params)
    rows = cursor.fetchall()
    new_rows = []
    for row in rows:
        new_rows.append([str(v) if v is None else v for v in row])
    data = [dict(zip(view.keys, values)) for values in new_rows]
    db.close()
    return data
