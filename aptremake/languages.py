
import render

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

    def __init__(self, data):
        self.task = Task.position
        self.data = data
        self.marks = render.Marks()
        self.marks.hpos = data.domain
        self.haxis = render.HorizontalAxis(data.range)

    @classmethod
    def can_express(self, relation):
        return SinglePosition.can_encode(relation)

    def __repr__(self):
        return "".join(["HorizontalAxis<", str(self.data), ">"])


class VerticalAxis(SinglePosition):
    
    def __init__(self, data):
        self.task = Task.position
        self.data = data
        self.marks = render.Marks()
        self.marks.vpos = data.domain
        self.vaxis = render.HorizontalAxis(data.range)
    
    @classmethod
    def can_express(self, relation):
        return SinglePosition.can_encode(relation)

    def __repr__(self):
        return "".join(["VerticalAxis<", str(self.data), ">"])


class LineChart(ApposedPosition):
    
    def __init__(self, data):
        self.task = Task.slope
        self.data = data
        self.haxis = render.HorizontalAxis(data.independent)
        self.vaxis = render.VerticalAxis(data.dependent)

    @classmethod
    def can_express(self, relation):
        return ApposedPosition.can_encode(relation)

    def __repr__(self):
        return "".join(["LineChart<", str(self.data), ">"])


class BarChart(ApposedPosition):
    
    def __init__(self, data):
        self.task = Task.length
        self.data = data
        # FIXME: What are the marks in these cases?
        self.haxis = render.HorizontalAxis(data.independent)
        self.vaxis = render.VerticalAxis(data.dependent)
    
    @classmethod
    def can_express(self, relation):
        return ApposedPosition.can_encode(relation)

    def __repr__(self):
        return "".join(["BarChart<", str(self.data), ">"])


class PlotChart(ApposedPosition):

    def __init__(self, data):
        self.task = Task.position
        self.data = data
        self.haxis = render.HorizontalAxis(data.independent)
        self.vaxis = render.VerticalAxis(data.dependent)
    
    @classmethod
    def can_express(self, relation):
        return ApposedPosition.can_encode(relation)

    def __repr__(self):
        return "".join(["PlotChart<", str(self.data), ">"])


class Color(RetinalList):
    
    def __init__(self, data):
        self.task = Task.hue
        self.data = data
        self.marks = render.Marks()
        self.marks.color = data
        if isinstance(self.data, FunctionalDependency):
            self.marks.color = data.range

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

    def __repr__(self):
        return "".join(["Color<", str(self.data), ">"])


class Shape(RetinalList):
    
    def __init__(self, data):
        self.task = Task.shape
        self.data = data
        self.marks = render.Marks()
        self.marks.shape = data
        if isinstance(self.data, FunctionalDependency):
            self.marks.shape = data.range
    
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

    def __repr__(self):
        return "".join(["Shape<", str(self.data), ">"])


class Size(RetinalList):
    
    def __init__(self, data):
        self.task = Task.area
        self.data = data
        self.marks = render.Marks()
        self.marks.size = data
        if isinstance(self.data, FunctionalDependency):
            self.marks.size = data.range
    
    @classmethod
    def can_express(self, relation):
        if RetinalList.can_encode(relation):
            if (isinstance(relation, FunctionalDependency) \
                and not relation.range.type == Type.nominal) \
                or \
                (isinstance(relation, Set) \
                and not relation.type == Type.nominal):
                return True
        return False

    def __repr__(self):
        return "".join(["Size<", str(self.data), ">"])


class Saturation(RetinalList):
    
    def __init__(self, data):
        self.task = Task.saturation
        self.data = data
        self.marks = render.Marks()
        self.marks.saturation = data
        if isinstance(self.data, FunctionalDependency):
            self.marks.saturation = data.range
    
    @classmethod
    def can_express(self, relation):
        if RetinalList.can_encode(relation):
            if (isinstance(relation, FunctionalDependency) \
                and not relation.range.type == Type.nominal) \
                or \
                (isinstance(relation, Set) \
                and not relation.type == Type.nominal):
                return True
        return False

    def __repr__(self):
        return "".join(["Saturation<", str(self.data), ">"])


class Texture(RetinalList):
    
    def __init__(self, data):
        self.task = Task.texture
        self.data = data
        self.marks = render.Marks()
        self.marks.texture = data
        if isinstance(self.data, FunctionalDependency):
            self.marks.texture = data.range
    
    @classmethod
    def can_express(self, relation):
        if RetinalList.can_encode(relation):
            if (isinstance(relation, FunctionalDependency) \
                and not relation.range.type == Type.quantitative) \
                or \
                (isinstance(relation, Set) \
                and not relation.type == Type.quantitative):
                return True
        return False

    def __repr__(self):
        return "".join(["Texture<", str(self.data), ">"])


class Orientation(RetinalList):
    
    def __init__(self, data):
        self.task = Task.angle
        self.data = data
        self.marks = render.Marks()
        self.marks.orientation = data
        if isinstance(self.data, FunctionalDependency):
            self.marks.orientation = data.range
    
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

    def __repr__(self):
        return "".join(["Orientation<", str(self.data), ">"])


class RoadMap(Map):
    
    def __init__(self, data):
        self.task = Task.position
        self.data = data
    
    @classmethod
    def can_express(self, relation):
        return Map.can_encode(relation)

    def __repr__(self):
        return "".join(["RoadMap<", str(self.data), ">"])


class TopographicMap(Map):
    
    def __init__(self, data):
        self.task = Task.density
        self.data = data
    
    @classmethod
    def can_express(self, relation):
        return Map.can_encode(relation)

    def __repr__(self):
        return "".join(["TopographicMap<", str(self.data), ">"])


class Tree(Connection):
    
    def __init__(self, data):
        self.task = Task.connection
        self.data = data
    
    @classmethod
    def can_express(self, relation):
        return Connection.can_encode(relation)

    def __repr__(self):
        return "".join(["Tree<", str(self.data), ">"])


class AcyclicGraph(Connection):

    def __init__(self, data):
        self.task = Task.connection
        self.data = data
    
    @classmethod
    def can_express(self, relation):
        return Connection.can_encode(relation)

    def __repr__(self):
        return "".join(["AcyclicGraph<", str(self.data), ">"])


class Network(Connection):
    
    def __init__(self, data):
        self.task = Task.connection
        self.data = data
    
    @classmethod
    def can_express(self, relation):
        return Connection.can_encode(relation)

    def __repr__(self):
        return "".join(["Network<", str(self.data), ">"])


class PieChart(Miscellaneous):
    
    def __init__(self, data):
        self.task = Task.angle
        self.data = data
    
    @classmethod
    def can_express(self, relation):
        return Miscellaneous.can_encode(relation)

    def __repr__(self):
        return "".join(["PieChart<", str(self.data), ">"])


class VennDiagram(Miscellaneous):
    
    def __init__(self, data):
        self.task = Task.area
        self.data = data
    
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

