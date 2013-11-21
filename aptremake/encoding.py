
from data import CartesianProduct, FunctionalDependency, Set, Type

class Encoding(object):

    @classmethod
    def can_encode(self, relation):
        return False

class SinglePosition(Encoding):

    @classmethod # NOTE: I have deviated from the original here by allowing
    def can_encode(self, relation): # sets to be encoded.
        # ORIGINAL:
        #if (isinstance(relation, FunctionalDependency) \
        #        and relation.determinant.type == Type.nominal):
        if isinstance(relation, Set) or \
           (isinstance(relation, FunctionalDependency) \
                and relation.determinant.type == Type.nominal):
            return True
        return False

class ApposedPosition(Encoding):
    
    @classmethod
    def can_encode(self, relation): # FIXME: I think this is wrong in the original
        # ORIGINAL:
        #if (isinstance(relation, CartesianProduct) \
        #        and not relation.sets[0].type == Type.nominal \
        #        and not relation.sets[1].type == Type.nominal):
        if (isinstance(relation, FunctionalDependency)) \
            or (isinstance(relation, CartesianProduct) \
                and not relation.sets[0].type == Type.nominal \
                and not relation.sets[1].type == Type.nominal):
            return True

class RetinalList(Encoding):
    
    @classmethod
    def can_encode(self, relation):
        if (isinstance(relation, Set) \
                    and not relation.type == Type.quantitative) \
                or (isinstance(relation, FunctionalDependency) \
                    and not relation.determinant.type == Type.quantitative):
            return True
        return False

class Map(Encoding):
    
    @classmethod
    def can_encode(self, relation):
        if (isinstance(relation, FunctionalDependency) \
                and relation.determinant.type == Type.location):
            return True
        return False

class Connection(Encoding):
    
    @classmethod
    def can_encode(self, relation):
        return False

class Miscellaneous(Encoding):
    
    @classmethod
    def can_encode(self, relation):
        return False

encodings = [SinglePosition, ApposedPosition, RetinalList, Map, Connection, Miscellaneous]

