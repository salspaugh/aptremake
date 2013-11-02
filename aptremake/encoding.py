
from data import FunctionalDependency, Set, Type

class Encoding(object):

    @classmethod
    def can_encode(self, partition):
        return False

class SinglePosition(Encoding):

    @classmethod
    def can_encode(self, partition):
        if (isinstance(partition, FunctionalDependency) \
            and partition.domain.type == Type.nominal):
                return True
        return False

class ApposedPosition(Encoding):
    
    @classmethod
    def can_encode(self, partition):
        return False

class RetinalList(Encoding):
    
    @classmethod
    def can_encode(self, partition):
        if (isinstance(partition, Set) \
                and not partition.type == Type.quantitative) \
            or (isinstance(partition, FunctionalDependency) \
                and not partition.domain.type == Type.quantitative):
            return True
        return False

class Map(Encoding):
    
    @classmethod
    def can_encode(self, partition):
        if (isinstance(partition, FunctionalDependency) \
            and partition.domain.type == Type.location):
            return True
        return False

class Connection(Encoding):
    
    @classmethod
    def can_encode(self, partition):
        return False

class Miscellaneous(Encoding):
    
    @classmethod
    def can_encode(self, partition):
        return False

encodings = [SinglePosition, ApposedPosition, RetinalList, Map, Connection, Miscellaneous]

