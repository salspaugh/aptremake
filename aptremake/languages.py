
from encoding import SinglePosition, ApposedPosition, RetinalList, Map, Connection, Miscellaneous
from data import *

class Task(object):
    
    position = "POSITION"
    length = "LENGTH"
    angle = "ANGLE"
    slope = "SLOPE"
    area = "AREA"
    volume = "VOLUME"
    density = "DENSITY"
    saturation = "SATURATION"
    hue = "HUE"
    texture = "TEXTURE"
    connection = "CONNECTION"
    containment = "CONTAINMENT"
    shape = "SHAPE"

class HorizontalAxis(SinglePosition):

    def __init__(self):
        self.task = Task.position
    
    @classmethod
    def can_express(self, partition):
        return SinglePosition.can_encode(partition)

class VerticalAxis(SinglePosition):
    
    def __init__(self):
        self.task = Task.position
    
    @classmethod
    def can_express(self, partition):
        return SinglePosition.can_encode(partition)

class LineChart(ApposedPosition):
    
    def __init__(self):
        self.task = Task.slope

    @classmethod
    def can_express(self, partition):
        return ApposedPosition.can_encode(partition)

class BarChart(ApposedPosition):
    
    def __init__(self):
        self.task = Task.length
    
    @classmethod
    def can_express(self, partition):
        return ApposedPosition.can_encode(partition)

class PlotChart(ApposedPosition):

    def __init__(self):
        self.task = Task.position
    
    @classmethod
    def can_express(self, partition):
        return ApposedPosition.can_encode(partition)

class Color(RetinalList):
    
    def __init__(self):
        self.task = Task.hue
    
    @classmethod
    def can_express(self, partition):
        if RetinalList.can_encode(partition):
            if (isinstance(partition, FunctionalDependency) \
                and partition.range.type == Type.nominal) \
                or \
                (isinstance(partition, Set) \
                and partition.type == Type.nominal):
                return True
        return False


class Shape(RetinalList):
    
    def __init__(self):
        self.task = Task.shape
    
    @classmethod
    def can_express(self, partition):
        if RetinalList.can_encode(partition):
            if (isinstance(partition, FunctionalDependency) \
                and partition.range.type == Type.nominal) \
                or \
                (isinstance(partition, Set) \
                and partition.type == Type.nominal):
                return True
        return False

class Size(RetinalList):
    
    def __init__(self):
        self.task = Task.area
    
    @classmethod
    def can_express(self, partition):
        if RetinalList.can_encode(partition):
            if (isinstance(partition, FunctionalDependency) \
                and not partition.range.type == Type.nominal) \
                or \
                (isinstance(partition, Set) \
                and not partition.type == Type.nominal):
                return True
        return False

class Saturation(RetinalList):
    
    def __init__(self):
        self.task = Task.saturation
    
    @classmethod
    def can_express(self, partition):
        if RetinalList.can_encode(partition):
            if (isinstance(partition, FunctionalDependency) \
                and not partition.range.type == Type.nominal) \
                or \
                (isinstance(partition, Set) \
                and not partition.type == Type.nominal):
                return True
        return False

class Texture(RetinalList):
    
    def __init__(self):
        self.task = Task.texture
    
    @classmethod
    def can_express(self, partition):
        if RetinalList.can_encode(partition):
            if (isinstance(partition, FunctionalDependency) \
                and not partition.range.type == Type.quantitative) \
                or \
                (isinstance(partition, Set) \
                and not partition.type == Type.quantitative):
                return True
        return False

class Orientation(RetinalList):
    
    def __init__(self):
        self.task = Task.angle
    
    @classmethod
    def can_express(self, partition):
        if RetinalList.can_encode(partition):
            if (isinstance(partition, FunctionalDependency) \
                and partition.range.type == Type.nominal) \
                or \
                (isinstance(partition, Set) \
                and partition.type == Type.nominal):
                return True
        return False

class RoadMap(Map):
    
    def __init__(self):
        self.task = Task.position
    
    @classmethod
    def can_express(self, partition):
        return Map.can_encode(partition)

class TopographicMap(Map):
    
    def __init__(self):
        self.task = Task.density
    
    @classmethod
    def can_express(self, partition):
        return Map.can_encode(partition)

class Tree(Connection):
    
    def __init__(self):
        self.task = Task.connection
    
    @classmethod
    def can_express(self, partition):
        return Connection.can_encode(partition)

class AcyclicGraph(Connection):

    def __init__(self):
        self.task = Task.connection
    
    @classmethod
    def can_express(self, partition):
        return Connection.can_encode(partition)

class Network(Connection):
    
    def __init__(self):
        self.task = Task.connection
    
    @classmethod
    def can_express(self, partition):
        return Connection.can_encode(partition)

class PieChart(Miscellaneous):
    
    def __init__(self):
        self.task = Task.angle
    
    @classmethod
    def can_express(self, partition):
        return Miscellaneous.can_encode(partition)

class VennDiagram(Miscellaneous):
    
    def __init__(self):
        self.task = Task.area
    
    @classmethod
    def can_express(self, partition):
        return Miscellaneous.can_encode(partition)

_languages = [
    HorizontalAxis,
    VerticalAxis,
    LineChart,
    BarChart,
    PlotChart,
    Color,
    Shape,
    Size,
    Saturation,
    Texture,
    Orientation,
    RoadMap,
    TopographicMap,
    Tree,
    AcyclicGraph,
    Network,
    PieChart,
    VennDiagram
]

