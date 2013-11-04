

class HorizontalAxis(object):

    def __init__(self, data):
        self.data = data

    def compose(self, more):
        pass

class VerticalAxis(object):
    
    def __init__(self, data):
        self.data = data

class Marks(object):

    def __init__(self):
        self.hpos = None
        self.vpos = None
        self.color = None
        self.shape = None
        self.size = None
        self.texture = None
        self.orientation = None
        self.saturation = None

    def compose(self, other):
        if (other.hpos and self.hpos) or \
            (other.vpos and self.vpos) or \
            (other.color and self.color) or \
            (other.shape and self.shape) or \
            (other.size and self.size) or \
            (other.texture and self.texture) or \
            (other.orientation and self.orientation) or \
            (other.saturation and self.saturation):
            return False
        if other.hpos and not self.hpos:
            self.hpos = other.hpos
        if other.vpos and not self.vpos:
            self.vpos = other.vpos
        if other.color and not self.color:
            self.color = other.color
        if other.shape and not self.shape:
            self.shape = other.shape
        if other.size and not self.size:
            self.size = other.size
        if other.texture and not self.texture:
            self.texture = other.texture
        if other.orientation and not self.orientation:
            self.orientation = other.orientation
        if other.saturation and not self.saturation:
            self.saturation = other.saturation
        return True
