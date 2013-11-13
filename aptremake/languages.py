
from encoding import SinglePosition, ApposedPosition, RetinalList, Map, Connection, Miscellaneous
from data import *
from composition import Objects, Encodes, Design


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

    task = Task.position

    @classmethod
    def can_express(cls, relation):
        return SinglePosition.can_encode(relation)

    @classmethod
    def design(cls, relation):
        marks = Encodes(Objects.marks, relation.domain, cls)
        hpos = Encodes(Objects.hpos, relation, cls)
        haxis = Encodes(Objects.haxis, relation.range, cls)
        return Design([marks, hpos, haxis])

class VerticalAxis(SinglePosition):
    
    task = Task.position
    
    @classmethod
    def can_express(cls, relation):
        return SinglePosition.can_encode(relation)

    @classmethod
    def design(cls, relation):
        marks = Encodes(Objects.marks, relation.domain, cls)
        vpos = Encodes(Objects.vpos, relation, cls)
        vaxis = Encodes(Objects.vaxis, relation.range, cls)
        return Design([marks, vpos, vaxis])


#class LineChart(ApposedPosition):
#    
#    
#    task = Task.slope
#
#    @classmethod
#    def can_express(cls, relation):
#        return ApposedPosition.can_encode(relation)
#
#
#class BarChart(ApposedPosition):
#    
#    
#    task = Task.length
#    
#    @classmethod
#    def can_express(cls, relation):
#        return ApposedPosition.can_encode(relation)
#
#
#class PlotChart(ApposedPosition):
#
#    
#    task = Task.position
#    
#    @classmethod
#    def can_express(cls, relation):
#        return ApposedPosition.can_encode(relation)
#

class Color(RetinalList):
    
    
    task = Task.hue

    @classmethod
    def can_express(cls, relation):
        if RetinalList.can_encode(relation):
            if (isinstance(relation, FunctionalDependency) \
                and (relation.range.type == Type.nominal \
                    or (relation.range.type == Type.ordinal and len(relation.range.tuples) < 11))) \
                or \
                (isinstance(relation, Set) \
                and (relation.type == Type.nominal \
                    or (relation.type == Type.ordinal and len(relation.tuples) < 11))):
                return True
        return False
    
    @classmethod
    def design(cls, relation):
        if isinstance(relation, FunctionalDependency):
            marks = Encodes(Objects.marks, relation.domain, cls)
            color = Encodes(Objects.color, relation, cls)
            return Design([marks, color])
        if isinstance(relation, Set):
            marks = Encodes(Objects.marks, relation, cls)
            color = Encodes(Objects.color, relation, cls)
            return Design([marks, color])


#class Shape(RetinalList):
#    
#    
#    task = Task.shape
#    
#    @classmethod
#    def can_express(cls, relation):
#        if RetinalList.can_encode(relation):
#            if (isinstance(relation, FunctionalDependency) \
#                and relation.range.type == Type.nominal) \
#                or \
#                (isinstance(relation, Set) \
#                and relation.type == Type.nominal):
#                return True
#        return False
#
#
#class Size(RetinalList):
#    
#    
#    task = Task.area
#    
#    @classmethod
#    def can_express(cls, relation):
#        if RetinalList.can_encode(relation):
#            if (isinstance(relation, FunctionalDependency) \
#                and not relation.range.type == Type.nominal) \
#                or \
#                (isinstance(relation, Set) \
#                and not relation.type == Type.nominal):
#                return True
#        return False
#
#
#class Saturation(RetinalList):
#    
#    
#    task = Task.saturation
#    
#    @classmethod
#    def can_express(cls, relation):
#        if RetinalList.can_encode(relation):
#            if (isinstance(relation, FunctionalDependency) \
#                and not relation.range.type == Type.nominal) \
#                or \
#                (isinstance(relation, Set) \
#                and not relation.type == Type.nominal):
#                return True
#        return False
#
#
#class Texture(RetinalList):
#    
#    
#    task = Task.texture
#    
#    @classmethod
#    def can_express(cls, relation):
#        if RetinalList.can_encode(relation):
#            if (isinstance(relation, FunctionalDependency) \
#                and not relation.range.type == Type.quantitative) \
#                or \
#                (isinstance(relation, Set) \
#                and not relation.type == Type.quantitative):
#                return True
#        return False
#
#
#class Orientation(RetinalList):
#    
#    
#    task = Task.angle
#    
#    @classmethod
#    def can_express(cls, relation):
#        if RetinalList.can_encode(relation):
#            if (isinstance(relation, FunctionalDependency) \
#                and relation.range.type == Type.nominal) \
#                or \
#                (isinstance(relation, Set) \
#                and relation.type == Type.nominal):
#                return True
#        return False
#
#
class RoadMap(Map):
    
    
    task = Task.position
    
    @classmethod
    def can_express(cls, relation):
        return Map.can_encode(relation)


class TopographicMap(Map):
    
    
    task = Task.density
    
    @classmethod
    def can_express(cls, relation):
        return Map.can_encode(relation)


class Tree(Connection):
    
    
    task = Task.connection
    
    @classmethod
    def can_express(cls, relation):
        return Connection.can_encode(relation)


class AcyclicGraph(Connection):

    
    task = Task.connection
    
    @classmethod
    def can_express(cls, relation):
        return Connection.can_encode(relation)


class Network(Connection):
    
    
    task = Task.connection
    
    @classmethod
    def can_express(cls, relation):
        return Connection.can_encode(relation)


class PieChart(Miscellaneous):
    
    
    task = Task.angle
    
    @classmethod
    def can_express(cls, relation):
        return Miscellaneous.can_encode(relation)


class VennDiagram(Miscellaneous):
    
    
    task = Task.area
    
    @classmethod
    def can_express(cls, relation):
        return Miscellaneous.can_encode(relation)


_languages = [
    HorizontalAxis,
    VerticalAxis,
#    LineChart,
#    BarChart,
#    PlotChart,
    Color,
#    Shape,
#    Size,
#    Saturation,
#    Texture,
#    Orientation,
#    RoadMap,
#    TopographicMap,
#    Tree,
#    AcyclicGraph,
#    Network,
#    PieChart,
#    VennDiagram
]

