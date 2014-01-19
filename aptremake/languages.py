
from encoding import SinglePosition, ApposedPosition, RetinalList, Map, Connection, Miscellaneous
from metadata import *
from design import *
from collections import OrderedDict


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
    mark = "MARK"


class HorizontalAxis(SinglePosition):

    task = Task.position

    @classmethod
    def can_express(cls, relation):
        return SinglePosition.can_encode(relation)

    @classmethod
    def design(cls, relation):
        subplot = Subplot(Marks["POINTS"](relation.determinant.name))
        subplot.haxis = True
        subplot.hpos = subplot.hlabel = relation.dependent.name
        subplot.hordering = relation.dependent.ordering
        subplot.hpos_nominal = relation.dependent.type == Type.nominal
        subplot.hpos_ordinal = relation.dependent.type == Type.ordinal
        d = Design(subplots={(0,0): subplot}) 
        d.tasks[relation.determinant.name] = (relation.determinant.type, Task.mark)
        d.tasks[relation.dependent.name] = (relation.dependent.type, Task.position)
        #d.tasks[None] = (None, Task.position)
        return d

class VerticalAxis(SinglePosition):
    
    task = Task.position
    
    @classmethod
    def can_express(cls, relation):
        return SinglePosition.can_encode(relation)

    @classmethod
    def design(cls, relation):
        subplot = Subplot(Marks["POINTS"](relation.determinant.name))
        subplot.vaxis = True
        subplot.vpos = subplot.vlabel = relation.dependent.name
        subplot.vordering = relation.dependent.ordering
        subplot.vpos_nominal = relation.dependent.type == Type.nominal
        subplot.vpos_ordinal = relation.dependent.type == Type.ordinal
        d = Design(subplots={(0,0): subplot}) 
        d.tasks[relation.determinant.name] = (relation.determinant.type, Task.mark)
        d.tasks[relation.dependent.name] = (relation.dependent.type, Task.position)
        #d.tasks[None] = (None, Task.position)
        return d

#class LineChart(ApposedPosition):
#    
#    task = Task.slope
#
#    @classmethod
#    def can_express(cls, relation):
#        return ApposedPosition.can_encode(relation)


class BarChart(ApposedPosition):
    
    @classmethod
    def can_express(cls, relation):
        if ApposedPosition.can_encode(relation):
            if (isinstance(relation, FunctionalDependency) \
                and (relation.determinant.type == Type.nominal or relation.determinant.type == Type.ordinal) \
                and (relation.dependent.type == Type.ordinal or relation.dependent.type == Type.quantitative)):
                return True
        return False             

    @classmethod
    def design(cls, relation): # TODO: Hard-code in when it becomes a sideways bar chart.
        if isinstance(relation, FunctionalDependency):
            subplot = Subplot(Marks["BARS"](relation.determinant.name))
            subplot.haxis = True
            subplot.vaxis = True
            subplot.hpos = subplot.hlabel = relation.determinant.name
            subplot.hordering = relation.determinant.ordering
            subplot.hpos_nominal = relation.determinant.type == Type.nominal
            subplot.hpos_ordinal = relation.determinant.type == Type.ordinal
            subplot.vpos = subplot.vlabel = relation.dependent.name
            subplot.vordering = relation.dependent.ordering
            subplot.vpos_nominal = relation.dependent.type == Type.nominal
            subplot.vpos_ordinal = relation.dependent.type == Type.ordinal
            d = Design(subplots={(0,0): subplot}) 
            d.tasks[relation.determinant.name] = (relation.determinant.type, Task.position)
            d.tasks[relation.dependent.name] = (relation.dependent.type, Task.length)
            return d

#class PlotChart(ApposedPosition):
#
#    task = Task.position
#    
#    @classmethod
#    def can_express(cls, relation):
#        return ApposedPosition.can_encode(relation)


class Color(RetinalList):
    
    task = Task.hue

    @classmethod
    def can_express(cls, relation):
        if RetinalList.can_encode(relation):
            if (isinstance(relation, FunctionalDependency) \
                and (relation.dependent.type == Type.nominal \
                    or (relation.dependent.type == Type.ordinal and len(relation.dependent.domain) < 11))) \
                or \
                (isinstance(relation, Set) \
                and (relation.type == Type.nominal \
                    or (relation.type == Type.ordinal and len(relation.domain) < 11))):
                return True
        return False
    
    @classmethod
    def design(cls, relation):
        if isinstance(relation, FunctionalDependency):
            d = Design() 
            d.color = relation.dependent.name
            d.color_ordinal = relation.dependent.type == Type.ordinal
            d.cordering = relation.dependent.ordering
            d.tasks[relation.determinant.name] = (relation.determinant.type, Task.mark)
            d.tasks[relation.dependent.name] = (relation.dependent.type, Task.hue)
            return d
        if isinstance(relation, Set):
            d = Design() 
            d.color = relation.name
            d.color_ordinal = relation.type == Type.ordinal
            d.cordering = relation.ordering
            d.tasks[relation.name] = (relation.type, Task.hue)
            return d

#class Shape(RetinalList):
#    
#    
#    task = Task.shape
#    
#    @classmethod
#    def can_express(cls, relation):
#        if RetinalList.can_encode(relation):
#            if (isinstance(relation, FunctionalDependency) \
#                and relation.dependent.type == Type.nominal) \
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
#                and not relation.dependent.type == Type.nominal) \
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
#                and not relation.dependent.type == Type.nominal) \
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
#                and not relation.dependent.type == Type.quantitative) \
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
#                and relation.dependent.type == Type.nominal) \
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

