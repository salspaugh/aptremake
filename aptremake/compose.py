

class Sentence(object):

    def __init__(self):
        self.haxis = None
        self.vaxis = None
        self.marks = None

    def compose(language):
        """ 1. Nothing has been assigned."""
        if not self.haxis and not self.vaxis and not self.marks: 
            return False

        """ 2. Only the haxis has been assigned."""
        if self.haxis and not self.vaxis and not self.marks:
            raise Exception # TODO: Make an exception class.

        """ 3. Only the vaxis has been assigned."""
        if not self.haxis and self.vaxis and not self.marks:
            raise Exception # TODO: Make an exception class.

        """ 4. Only the marks have been assigned."""
        if not self.haxis and not self.vaxis and self.marks:
            return False

        """ 5. The haxis and marks have been assigned."""
        if self.haxis and not self.vaxis and self.marks:
            return False

        """ 6. The vaxis and marks have been assigned."""
        if not self.haxis and self.vaxis and self.marks:
            return False

        """ 7. The haxis and vaxis have been assigned."""
        if self.haxis and self.vaxis and not self.marks:
            return False

        """ 8. All three have been assigned."""
        if self.haxis and self.vaxis and self.marks:
            return False

    def __repr__(self):
        return "Sentence"
