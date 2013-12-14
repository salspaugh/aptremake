
from aptremake.data import *
from aptremake.db import *
import sys

def insert(db, table, vals):
    cursor = db.cursor()
    nvals = len(vals)
    statement = "".join(["INSERT INTO %s (", ", ".join(["%s"]*nvals), ") VALUES (", ", ".join(["?"]*nvals), ")"])
    strs = [table] + [x[0] for x in vals]
    statement = statement % tuple(strs)
    cursor.execute(statement, [x[1] for x in vals])
    db.commit()

def load(specfilename):
    database, table, data = read_data(specfilename)
    db = connect_db(database)
    tuples = {}
    for (name, relation) in data.iteritems():
        if isinstance(relation, FunctionalDependency):
            determinant = relation.determinant.name
            dependent = relation.dependent.name
            for (det, dep) in relation.tuples:
                if det not in tuples:
                    tuples[det] = {}
                tuples[det][determinant] = det
                tuples[det][dependent] = dep
    for (key, vals) in tuples.iteritems():
        insert(db, table, vals.items())
    db.close()
    
load(sys.argv[1])

