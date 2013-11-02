
from encoding import SinglePosition, ApposedPosition, RetinalList, Map, Connection, Miscellaneous

class HorizontalAxis(SinglePosition):
    pass

class VerticalAxis(SinglePosition):
    pass

class LineChart(ApposedPosition):
    pass

class BarChart(ApposedPosition):
    pass

class PlotChart(ApposedPosition):
    pass

class Color(RetinalList):
    pass

class Shape(RetinalList):
    pass

class Size(RetinalList):
    pass

class Saturation(RetinalList):
    
    @classmethod
    def can_express(self, partition):
        if RetinalList.can_encode(self, partition):
            pass

class Texture(RetinalList):
    pass

class Orientation(RetinalList):
    pass

class RoadMap(Map):
    pass

class TopographicMap(Map):
    pass

class Tree(Connection):
    pass

class AcyclicGraph(Connection):
    pass

class Network(Connection):
    pass

class PieChart(Miscellaneous):
    pass

class VennDiagram(Miscellanous):
    pass
