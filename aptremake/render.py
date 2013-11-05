

class HorizontalAxis(object):

    def __init__(self, data):
        self.data = data

    def compose(self, other):
        pass

class VerticalAxis(object):
    
    def __init__(self, data):
        self.data = data

class Marks(object):

    def __init__(self):
        self.hpos = None
        self.vpos = None
        self.color = None
        #self.shape = None
        #self.size = None
        #self.texture = None
        #self.orientation = None
        #self.saturation = None

    def nothing_assigned(self):
        return not (self.hpos and self.vpos and self.color)

    def assign_all(self, other):
        try:
            self.hpos = [other.hpos]
        except: # TODO: Catch the correct error here.
            pass
        try:
            self.vpos = [other.vpos]
        except:
            pass
        try:
            self.color = [other.color]
        except:
            pass
        return True

    def compose(self, other):
        if self.nothing_assigned():
            return self.assign_all(other)

        if self.hpos and not self.vpos and not self.color:
            if other.hpos and not other.vpos and not other.color:
                return False
            if not other.hpos and other.vpos and not other.color:
                return False
            if not other.hpos and not other.vpos and other.color:
                return False
            if other.hpos and other.vpos and not other.color:
                return False
            if other.hpos and not other.vpos and other.color:
                return False
            if not other.hpos and other.vpos and other.color:
                return False
            if other.hpos and other.vpos and other.color:
                return False

        if not self.hpos and self.vpos and not self.color:
            if other.hpos and not other.vpos and not other.color:
                return False
            if not other.hpos and other.vpos and not other.color:
                return False
            if not other.hpos and not other.vpos and other.color:
                return False
            if other.hpos and other.vpos and not other.color:
                return False
            if other.hpos and not other.vpos and other.color:
                return False
            if not other.hpos and other.vpos and other.color:
                return False
            if other.hpos and other.vpos and other.color:
                return False

        if not self.hpos and not self.vpos and self.color:
            if other.hpos and not other.vpos and not other.color:
                return False
            if not other.hpos and other.vpos and not other.color:
                return False
            if not other.hpos and not other.vpos and other.color:
                return False
            if other.hpos and other.vpos and not other.color:
                return False
            if other.hpos and not other.vpos and other.color:
                return False
            if not other.hpos and other.vpos and other.color:
                return False
            if other.hpos and other.vpos and other.color:
                return False
     
        if self.hpos and self.vpos and not self.color:
            return False
        if self.hpos and not self.vpos and self.color:
            return False
        if not self.hpos and self.vpos and self.color:
            return False

        if self.hpos and self.vpos and self.color:
            return False
