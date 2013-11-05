
import render

from encoding import SinglePosition, ApposedPosition, RetinalList, Map, Connection, Miscellaneous
from data import *

class Objects(object):
    
    haxis = "HAXIS"
    vaxis = "VAXIS"
    hpos = "HPOS"
    vpos = "VPOS"
    color = "COLOR"
    

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
    def can_express(self, relation):
        return SinglePosition.can_encode(relation)

    @classmethod
    def design(self, relation):
        marks = Encodes(Objects.hpos, relation, self)
        axis = Encodes(Objects.haxis, relation.range.domain, self)
        return Design([marks, axis])

    def __repr__(self):
        return "".join(["HorizontalAxis<", str(self.data), ">"])


class VerticalAxis(SinglePosition):
    
    def __init__(self):
        self.task = Task.position
    
    @classmethod
    def can_express(self, relation):
        return SinglePosition.can_encode(relation)

    @classmethod
    def design(self, relation):
        marks = Encodes(Objects.vpos, relation, self)
        axis = Encodes(Objects.vaxis, relation.range.domain, self)
        return Design([marks, axis])

    def __repr__(self):
        return "".join(["VerticalAxis<", str(self.data), ">"])


#class LineChart(ApposedPosition):
#    
#    def __init__(self):
#        self.task = Task.slope
#
#    @classmethod
#    def can_express(self, relation):
#        return ApposedPosition.can_encode(relation)
#
#    def __repr__(self):
#        return "".join(["LineChart<", str(self.data), ">"])
#
#
#class BarChart(ApposedPosition):
#    
#    def __init__(self):
#        self.task = Task.length
#    
#    @classmethod
#    def can_express(self, relation):
#        return ApposedPosition.can_encode(relation)
#
#    def __repr__(self):
#        return "".join(["BarChart<", str(self.data), ">"])
#
#
#class PlotChart(ApposedPosition):
#
#    def __init__(self):
#        self.task = Task.position
#    
#    @classmethod
#    def can_express(self, relation):
#        return ApposedPosition.can_encode(relation)
#
#    def __repr__(self):
#        return "".join(["PlotChart<", str(self.data), ">"])


class Color(RetinalList):
    
    def __init__(self):
        self.task = Task.hue

    @classmethod
    def can_express(self, relation):
        if RetinalList.can_encode(relation):
            if (isinstance(relation, FunctionalDependency) \
                and relation.range.type == Type.nominal) \
                or \
                (isinstance(relation, Set) \
                and relation.type == Type.nominal):
                return True
        return False
    
    @classmethod
    def design(self, relation):
        marks = Encodes(Objects.color, relation, self)
        return Design([marks])

    def __repr__(self):
        return "".join(["Color<", str(self.data), ">"])


#class Shape(RetinalList):
#    
#    def __init__(self):
#        self.task = Task.shape
#    
#    @classmethod
#    def can_express(self, relation):
#        if RetinalList.can_encode(relation):
#            if (isinstance(relation, FunctionalDependency) \
#                and relation.range.type == Type.nominal) \
#                or \
#                (isinstance(relation, Set) \
#                and relation.type == Type.nominal):
#                return True
#        return False
#
#    def __repr__(self):
#        return "".join(["Shape<", str(self.data), ">"])
#
#
#class Size(RetinalList):
#    
#    def __init__(self):
#        self.task = Task.area
#    
#    @classmethod
#    def can_express(self, relation):
#        if RetinalList.can_encode(relation):
#            if (isinstance(relation, FunctionalDependency) \
#                and not relation.range.type == Type.nominal) \
#                or \
#                (isinstance(relation, Set) \
#                and not relation.type == Type.nominal):
#                return True
#        return False
#
#    def __repr__(self):
#        return "".join(["Size<", str(self.data), ">"])
#
#
#class Saturation(RetinalList):
#    
#    def __init__(self):
#        self.task = Task.saturation
#    
#    @classmethod
#    def can_express(self, relation):
#        if RetinalList.can_encode(relation):
#            if (isinstance(relation, FunctionalDependency) \
#                and not relation.range.type == Type.nominal) \
#                or \
#                (isinstance(relation, Set) \
#                and not relation.type == Type.nominal):
#                return True
#        return False
#
#    def __repr__(self):
#        return "".join(["Saturation<", str(self.data), ">"])
#
#
#class Texture(RetinalList):
#    
#    def __init__(self):
#        self.task = Task.texture
#    
#    @classmethod
#    def can_express(self, relation):
#        if RetinalList.can_encode(relation):
#            if (isinstance(relation, FunctionalDependency) \
#                and not relation.range.type == Type.quantitative) \
#                or \
#                (isinstance(relation, Set) \
#                and not relation.type == Type.quantitative):
#                return True
#        return False
#
#    def __repr__(self):
#        return "".join(["Texture<", str(self.data), ">"])
#
#
#class Orientation(RetinalList):
#    
#    def __init__(self):
#        self.task = Task.angle
#    
#    @classmethod
#    def can_express(self, relation):
#        if RetinalList.can_encode(relation):
#            if (isinstance(relation, FunctionalDependency) \
#                and relation.range.type == Type.nominal) \
#                or \
#                (isinstance(relation, Set) \
#                and relation.type == Type.nominal):
#                return True
#        return False
#
#    def __repr__(self):
#        return "".join(["Orientation<", str(self.data), ">"])
#
#
class RoadMap(Map):
    
    def __init__(self):
        self.task = Task.position
    
    @classmethod
    def can_express(self, relation):
        return Map.can_encode(relation)

    def __repr__(self):
        return "".join(["RoadMap<", str(self.data), ">"])


class TopographicMap(Map):
    
    def __init__(self):
        self.task = Task.density
    
    @classmethod
    def can_express(self, relation):
        return Map.can_encode(relation)

    def __repr__(self):
        return "".join(["TopographicMap<", str(self.data), ">"])


class Tree(Connection):
    
    def __init__(self):
        self.task = Task.connection
    
    @classmethod
    def can_express(self, relation):
        return Connection.can_encode(relation)

    def __repr__(self):
        return "".join(["Tree<", str(self.data), ">"])


class AcyclicGraph(Connection):

    def __init__(self):
        self.task = Task.connection
    
    @classmethod
    def can_express(self, relation):
        return Connection.can_encode(relation)

    def __repr__(self):
        return "".join(["AcyclicGraph<", str(self.data), ">"])


class Network(Connection):
    
    def __init__(self):
        self.task = Task.connection
    
    @classmethod
    def can_express(self, relation):
        return Connection.can_encode(relation)

    def __repr__(self):
        return "".join(["Network<", str(self.data), ">"])


class PieChart(Miscellaneous):
    
    def __init__(self):
        self.task = Task.angle
    
    @classmethod
    def can_express(self, relation):
        return Miscellaneous.can_encode(relation)

    def __repr__(self):
        return "".join(["PieChart<", str(self.data), ">"])


class VennDiagram(Miscellaneous):
    
    def __init__(self):
        self.task = Task.area
    
    @classmethod
    def can_express(self, relation):
        return Miscellaneous.can_encode(relation)

    def __repr__(self):
        return "".join(["VennDiagram<", str(self.data), ">"])


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

