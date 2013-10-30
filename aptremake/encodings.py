
from data import FunctionalDependency, Set

class SinglePosition(object):

    @classmethod
    def meets_criteria(partition):
        if (isinstance(partition) == FunctionalDependency \
            and partition.domain.type == "NOMINAL"):
                return True
        return False

class ApposedPosition(object):
    
    @classmethod
    def meets_criteria(partition):
        return False

class RetinalList(object):
    
    @classmethod
    def meets_criteria(partition):
        if (isinstance(partition) == Set \
                and not partition.type == "QUANTITATIVE") \
            or (isinstance(partition) == FunctionalDependency \
                and not partition.domain.type == "QUANTITATIVE"):
            return True
        return False

class Map(object):
    
    @classmethod
    def meets_criteria(partition):
        if (isinstance(partition) == FunctionalDependency \
            and partition.domain.type == "LOCATION"):
            return True
        return False

class Connection(object):
    
    @classmethod
    def meets_criteria(partition):
        return False

class Miscellaneous(object):
    
    @classmethod
    def meets_criteria(partition):
        return False

