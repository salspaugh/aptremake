
from encoding import SinglePosition, ApposedPosition, RetinalList, Map, Connection, Miscellaneous
from data import *
from composition import Objects, Encodes, Design
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
        if isinstance(relation, FunctionalDependency):
            marks = Encodes(Objects.marks, relation.determinant, cls)
            hpos = Encodes(Objects.hpos, relation, cls)
            haxis = Encodes(Objects.haxis, relation.dependent, cls)
            encodings = [marks, hpos, haxis]
            tasks = OrderedDict()
            tasks[relation.determinant.name] = (relation.determinant.type, Task.mark)
            tasks[relation.dependent.name] = (relation.dependent.type, Task.position)
            return Design(encodings, tasks)
        if isinstance(relation, Set): # TODO: Consider getting rid of this since
            marks = Encodes(Objects.marks, relation, cls) # it's not in the original
            hpos = Encodes(Objects.hpos, relation, cls)
            haxis = Encodes(Objects.haxis, relation, cls)
            encodings = [marks, hpos, haxis]
            tasks = OrderedDict()
            tasks[relation.name] = (relation.type, Task.position)
            return Design(encodings, tasks)
            

class VerticalAxis(SinglePosition):
    
    task = Task.position
    
    @classmethod
    def can_express(cls, relation):
        return SinglePosition.can_encode(relation)

    @classmethod
    def design(cls, relation):
        if isinstance(relation, FunctionalDependency):
            marks = Encodes(Objects.marks, relation.determinant, cls)
            vpos = Encodes(Objects.vpos, relation, cls)
            vaxis = Encodes(Objects.vaxis, relation.dependent, cls)
            encodings = [marks, vpos, vaxis]
            tasks = OrderedDict()
            tasks[relation.determinant.name] = (relation.determinant.type, Task.mark)
            tasks[relation.dependent.name] = (relation.dependent.type, Task.position)
            return Design(encodings, tasks)
        if isinstance(relation, Set): # TODO: Consider getting rid of this since
            marks = Encodes(Objects.marks, relation, cls) # it's not in the original
            vpos = Encodes(Objects.vpos, relation, cls)
            vaxis = Encodes(Objects.vaxis, relation, cls)
            encodings = [marks, vpos, vaxis]
            tasks = OrderedDict()
            tasks[relation.name] = (relation.type, Task.position)
            return Design(encodings, tasks)


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
            marks = Encodes(Objects.marks, relation.determinant, cls) 
            haxis = Encodes(Objects.haxis, relation.determinant, cls)
            hpos = Encodes(Objects.hpos, relation, cls)
            vaxis = Encodes(Objects.vaxis, relation.dependent, cls)
            vpos = Encodes(Objects.vpos, relation, cls)
            #height = Encodes(Objects.height, relation, cls)
            #width = Encodes(Objects.width, None, cls) # unconstrained
            marktype = Encodes(Objects.marktype, "bar", cls)
            #encodings = [marks, haxis, hpos, vaxis, vpos, height, width, marktype]
            encodings = [marks, haxis, hpos, vaxis, vpos, marktype]
            tasks = OrderedDict()
            tasks[relation.determinant.name] = (relation.determinant.type, Task.position)
            tasks[relation.dependent.name] = (relation.dependent.type, Task.length)
            return Design(encodings, tasks)

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
                    or (relation.dependent.type == Type.ordinal and len(relation.dependent.tuples) < 11))) \
                or \
                (isinstance(relation, Set) \
                and (relation.type == Type.nominal \
                    or (relation.type == Type.ordinal and len(relation.tuples) < 11))):
                return True
        return False
    
    @classmethod
    def design(cls, relation):
        if isinstance(relation, FunctionalDependency):
            marks = Encodes(Objects.marks, relation.determinant, cls)
            color = Encodes(Objects.color, relation, cls)
            encodings = [marks, color]
            tasks = OrderedDict()
            tasks[relation.determinant.name] = (relation.determinant.type, Task.mark)
            tasks[relation.dependent.name] = (relation.dependent.type, Task.hue)
            return Design(encodings, tasks)
        if isinstance(relation, Set):
            marks = Encodes(Objects.marks, relation, cls)
            color = Encodes(Objects.color, relation, cls)
            encodings = [marks, color]
            tasks = OrderedDict()
            tasks[relation.name] = (relation.type, Task.hue)
            return Design(encodings, tasks)


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
    BarChart,
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

